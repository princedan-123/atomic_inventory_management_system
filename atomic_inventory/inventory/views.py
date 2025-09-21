from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    Merchant, Sku, ProductCategory, Product, Order,
    Delivery, MissingProduct
    )
from .serializers import (
    MerchantSerializer, SkuSerializer,
    ProductCategorySerializer, ProductSerializer,
    OrderSerializer, DeliverySerializer,
    MissingProductSerializer
    )
from rest_framework import viewsets
from users.permissions import IsStockManager, AdminUser, IsAgent

class MerchantView(viewsets.ModelViewSet):
    """The view logic for Merchant entity."""
    permission_classes = [AdminUser | IsStockManager]
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

class SkuView(viewsets.ModelViewSet):
    """The view logic for Sku entity."""
    permission_classes = [AdminUser | IsStockManager]
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer

class ProductCategory(viewsets.ModelViewSet):
    """The view logic for Product categorization."""
    permission_classes = [AdminUser | IsStockManager]
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductView(viewsets.ModelViewSet):
    """The view logic for all crud operations on product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        """Grants permission to users based on request actions."""
        if self.action in ['list', 'create', 'retrieve']:
            permission_classes = [AdminUser | IsStockManager]
        else:
            permission_classes = [AdminUser]
        return [permission() for permission in permission_classes]

class OrderView(viewsets.ModelViewSet):
    """The view set for crud operations on order."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get_permissions(self):
        """Setting permissions based on request actions."""
        if self.action in ['create', 'destroy', 'retrieve']:
            permission_classes = [AdminUser | IsStockManager]
        elif self.action == 'list':
            permission_classes = [IsAgent | AdminUser | IsStockManager]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAgent]
        return [permission() for permission in permission_classes]
    
    def perform_update(self, serializer):
        """Removes product from the database upon order confirmation."""
        old_order = self.get_object()
        order_instance = serializer.save()
        product = order_instance.product
        if product.quantity < order_instance.quantity:
            order_instance.delete()
            raise Exception(f'Availiable stock is not enough')
        if order_instance.status == 'confirmed':
            product.quantity = product.quantity - order_instance.quantity
            product.save()
            print(f'product quantity {product.quantity}')
        if old_order.status != 'confirmed' and order_instance.status == 'confirmed':
            delivery, created_at = Delivery.objects.get_or_create(
                order=order_instance,
                defaults={
                    'status': 'pending'
                    }
                )
            print(f'this is the delivery {delivery}')

class ListAllDeliveries(APIView):
    """
    A view class for fetching all deliveries.
    It requires token authentication.
    Only the admin or stock manager has permission to get all deliveries.
    """
    permission_classes = [AdminUser]
    def get(self, request):
        """
        Fetches all deliveries.
        """
        deliveries = Delivery.objects.all()
        serialized_delivery = DeliverySerializer(deliveries, many=True)
        data = serialized_delivery.data
        return Response({
            'deliveries': data
            }, status=200)

class AgentDelivery(APIView):
    """
    A view that retrieves the delivery of a particular agent.
    Updates an agent delivery record.
    """
    permission_classes = [AdminUser | IsAgent | IsStockManager]
    def get(self, request, pk=None):
        """Retrieves an agent's delivery record."""
        if pk is None:
            return Response({
                'error': 'user id is missing!'
            }, status=400)
        deliveries = Delivery.objects.filter(order__assigned_to_id=pk)
        serialized_delivery = DeliverySerializer(deliveries, many=True)
        data = serialized_delivery.data
        return Response({
            f'{pk}': data
        }, status=200)

    def put(self, request, pk=None):
        """Updates an agent's delivery record."""
        if pk is None:
            return Response({
                'error': 'missing agent id'
            }, status=400)
        data = request.data
        if not data:
            return Response({
                'error': 'missing json payload'
            }, status=400)
        delivery_id = data.get('id')
        new_status = data.get('status')
        user = request.user
        if delivery_id and new_status == 'delivered':
            try:
                delivery = Delivery.objects.get(pk=delivery_id)
                if delivery.order.assigned_to != user:
                    return Response({
                        'invalid user': 'This record does not belong to this user'
                    }, status=403)
                if delivery.status == 'pending':
                    delivery.status = new_status
                    delivery.delivered_at = timezone.now()
                    delivery.save()
                    return Response({
                        'delivery_status': delivery.status
                        })
            except Delivery.DoesNotExist:
                return Response(
                    {'error': 'Delivery does not exist for this agent'}
                    )
        if delivery_id and new_status == 'failed':
            try:
                delivery = Delivery.objects.get(pk=delivery_id)
                if delivery.order.assigned_to != user:
                    return Response({
                        'invalid user': 'This record does not belong to this user'
                    }, status=403)
                if delivery.status == 'pending':
                    delivery.status = new_status
                    delivery.save()
                    #  file a missing product record upon failed delivery
                    MissingProduct.objects.create(
                        product = delivery.order.product,
                        delivery = delivery,
                        quantity = delivery.order.quantity,
                        reported_by = None,
                        assigned_to = delivery.order.assigned_to,
                        reason = 'delivery failed, this agent is yet to return this product'
                    )
            except Delivery.DoesNotExist:
                return Response(
                    {'error': 'Delivery does not exist for this agent'}
                    )    
        return Response({
            'error': 'no delivery id or status is invalid'
        }, status=400)

class ListMissingProducts(APIView):
    """
    A view that lists missing products.
    It uses token for authentication.
    Only admins and stock managers can access this view.
    """
    permission_classes = [AdminUser | IsStockManager]
    def get(self, request, pk=None):
        missing_products = MissingProduct.objects.all()
        serialized = MissingProductSerializer(missing_products, many=True)
        data  = serialized.data
        return Response({
            'missing': data
            }, status=200)

class ListMissing_per_agent(APIView):
    """
    Lists Missing products assigned to an agent.
    Token is needed for authentication.
    agents id is need to filter the agents record.
    """
    def get(self, request, pk=None):
        if pk is None:
            return Response({
                'error': 'Missing agents id'
                }, status=400)
        missing_products_per_agent = MissingProduct.objects.filter(assigned_to=pk)
        serialized = MissingProductSerializer(missing_products_per_agent, many=True)
        data = serialized.data
        return Response({
            'missing_per_agent': data
            },status=200)