from django import forms 
from .models import Product, Order



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        
        fields = ['name','description','category', 'quantity' ]
        
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity']
        
    def clean_order_quantity(self):
        order_quantity = self.cleaned_data.get('order_quantity')
        product = self.cleaned_data.get('product')
        
        if product and order_quantity > product.quantity:
            raise forms.ValidationError(f'Cannot order more than {product.quantity} items of {product.name}.')
        
        return order_quantity