from django.db import models
from django.conf import settings

order_status = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled')
]

delivery_status = [
    ('pending', 'Pending'),
    ('failed', 'Failed'),
    ('delivered', 'Delivered')
]

b_to_b_status = [
    ('initiated', 'Initiated'),
    ('confirmed', 'Confirmed'),
    ('rejected', 'Rejected')
]


class Merchant(models.Model):
    """Represents merchants who own products."""
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f'{self.first_name}'


class Sku(models.Model):
    """Unique identifier for a particular brand/product."""
    sku = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f'{self.sku}'


class ProductCategory(models.Model):
    """Categorization of a product."""
    category = models.CharField(max_length=250, unique=True, null=False)

    def __str__(self):
        return f'{self.category}'

class Product(models.Model):
    """Represents products in stock."""
    name = models.CharField(max_length=250)
    category = models.ForeignKey(
        ProductCategory, related_name='products', on_delete=models.CASCADE
    )
    merchant = models.ForeignKey(
        Merchant, related_name='products', on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False)
    received_at = models.DateTimeField(auto_now_add=True)
    sku = models.ForeignKey(
        Sku, related_name='products', on_delete=models.SET_NULL, null=True, blank=True
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='added_products',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    image = models.ImageField(upload_to='products/', null=True)

    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    """Represents an order."""
    product = models.ForeignKey(
        Product, related_name='orders', on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False)
    raised_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='raised_orders',
        on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=order_status, default='pending'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='assigned_orders',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f'{self.id}'

class Delivery(models.Model):
    """Represents a delivery made by an agent."""
    order = models.ForeignKey(
        Order, related_name='deliveries', on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10, choices=delivery_status, default='pending'
    )
    delivered_at = models.DateTimeField(null=True, blank=True)



class BtoB(models.Model):
    """Represents a B2B process."""
    delivery = models.ForeignKey(
        Delivery, related_name='b_to_b_records', on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20, choices=b_to_b_status, default='initiated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    initiated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='BtoB', null=False, blank=False
        )


class MissingProduct(models.Model):
    """Represents a missing product during delivery."""
    product = models.ForeignKey(
        Product, related_name='missing_reports', on_delete=models.CASCADE
    )
    delivery = models.ForeignKey(
        Delivery, related_name='missing_reports', on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=False)
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reported_missing_products',
        on_delete=models.SET_NULL, null=True
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='assigned_missing_products',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    reason = models.CharField(max_length=250)
