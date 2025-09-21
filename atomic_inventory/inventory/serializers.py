"""
A module that helps to translate database objects 
into Python native data types.
"""
from rest_framework import serializers
from .models import (
    Merchant, Sku, ProductCategory, Product,
    Order, Delivery, BtoB, MissingProduct
    )
from users.models import User


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'


class SkuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sku
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(), write_only=True
    )
    category_name = serializers.StringRelatedField(
        source="category", read_only=True
    )
    merchant = serializers.PrimaryKeyRelatedField(
        queryset=Merchant.objects.all(), write_only=True
    )
    merchant_name = serializers.StringRelatedField(
        source="merchant", read_only=True
    )
    sku = serializers.PrimaryKeyRelatedField(
        queryset=Sku.objects.all(), write_only=True
    )
    sku_name = serializers.StringRelatedField(source="sku", read_only=True)
    added_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    added_by_name = serializers.StringRelatedField(
        source="added_by", read_only=True
    )

    class Meta:
        model = Product
        fields = '__all__'

    def validate_quantity(self, value):
        """Ensure quantity is a positive number."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value

    def validate_unit_price(self, value):
        """Ensure price is a positive number."""
        if value <= 0:
            raise serializers.ValidationError("price must be greater than zero")
        return value

class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )
    product_name = serializers.StringRelatedField(
        source="product", read_only=True
    )

    raised_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    raised_by_name = serializers.StringRelatedField(
        source="raised_by", read_only=True
    )

    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, allow_null=False, required=True
    )
    assigned_to_name = serializers.StringRelatedField(
        source="assigned_to", read_only=True
    )
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def get_fields(self):
        """
        Overide default get_fields to only allow
        writes for status field.
        """
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.method in ['PUT', 'PATCH']:
            for field_name in fields:
                if field_name != 'status':
                    fields[field_name].read_only = True
        return fields

class DeliverySerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), write_only=True
    )
    order_id = serializers.StringRelatedField(source='order')

    class Meta:
        model = Delivery
        fields = '__all__'


class BtoBSerializer(serializers.ModelSerializer):
    delivery = serializers.PrimaryKeyRelatedField(
        queryset=Delivery.objects.all(), write_only=True
    )

    class Meta:
        model = BtoB
        fields = '__all__'


class MissingProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )
    product_name = serializers.StringRelatedField(
        source="product", read_only=True
    )

    delivery = serializers.PrimaryKeyRelatedField(
        queryset=Delivery.objects.all(), write_only=True, allow_null=True
    )

    reported_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, allow_null=True
    )
    reported_by_name = serializers.StringRelatedField(
        source="reported_by", read_only=True
    )

    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, allow_null=True, required=False
    )
    assigned_to_name = serializers.StringRelatedField(
        source="assigned_to", read_only=True
    )

    class Meta:
        model = MissingProduct
        fields = '__all__'