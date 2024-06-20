from django.contrib import admin
from .models import Category, Product, Order
from django.contrib.auth.models import Group
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'quantity',)
    list_filter = ('category',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product','staff','order_quantity', 'created_at')   

admin.site.site_header = 'Inventory Management System'
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
# admin.site.unregister(Group)