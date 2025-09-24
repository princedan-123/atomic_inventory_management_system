from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

order_router = DefaultRouter()
sku_router = DefaultRouter()
product_router = DefaultRouter()
merchant_router = DefaultRouter()
product_category_router = DefaultRouter()
sku_router.register('sku', views.SkuView)
merchant_router.register('merchant', views.MerchantView)
product_category_router.register('category', views.ProductCategory)
product_router.register('product', views.ProductView)
order_router.register('order', views.OrderView)


urlpatterns = [
    path('', include(sku_router.urls)),
    path('', include(merchant_router.urls)),
    path('', include(product_category_router.urls)),
    path('', include(product_router.urls)),
    path('', include(order_router.urls)),
    path('list/deliveries/all/', views.ListAllDeliveries.as_view()),
    path('list/deliveries/<int:pk>/', views.AgentDelivery.as_view()),
    path('make/delivery/<int:pk>/', views.AgentDelivery.as_view()),
    path('list/missing_per_agent/<int:pk>/', views.ListMissing_per_agent.as_view()),
    path('list/missing_products/all/', views.ListMissingProducts.as_view()),
    path('list/all_btob/', views.BtoBViewAdmin.as_view()),
    path('list/agent_btob/', views.BtoBView.as_view()),
    path('make/btob/', views.BtoBView.as_view()),
    path('confirm/btob/<int:pk>/', views.BtoBViewAdmin.as_view())
]