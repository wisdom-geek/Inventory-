from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.
from django.db import transaction, IntegrityError

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    
    class Meta:
        ordering = ['created_at',]
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)    
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    
    
    def __str__(self):
        return f"{self.name}"
    

class Order(models.Model):
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def save(self, *args, **kwargs):        
        with transaction.atomic():
            existing_order, created = Order.objects.select_for_update().get_or_create(
                product=self.product,
                staff=self.staff,
                defaults={'order_quantity': 0}  # Initialize order_quantity if it's a new order
            )

            total_quantity = existing_order.order_quantity + self.order_quantity
            if total_quantity > self.product.quantity:
                raise ValidationError(f"Cannot order more than available quantity for {self.product.name}.")

            existing_order.order_quantity = total_quantity
            existing_order.save()
                
    
    def __str__(self):
        staff_username = self.staff.username if self.staff else 'Unknown'
        return f'{self.product} ordered by {staff_username}'