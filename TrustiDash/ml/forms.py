from django import forms
from tdapp.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'product_price',
            'product_quantity',
            'product_brand',
            'product_category',
            'product_discount',
            'product_url'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Enter product name', 'class': 'form-control'}),
            'product_price': forms.NumberInput(attrs={'placeholder': 'Enter product price', 'class': 'form-control'}),
            'product_quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity', 'class': 'form-control'}),
            'product_brand': forms.TextInput(attrs={'placeholder': 'Enter brand name', 'class': 'form-control'}),
            'product_category': forms.TextInput(attrs={'placeholder': 'Enter category', 'class': 'form-control'}),
            'product_discount': forms.NumberInput(attrs={'placeholder': 'Enter discount (optional)', 'class': 'form-control'}),
            'product_url': forms.TextInput(attrs={'placeholder': 'Give Product Image URL', 'class': 'form-control'}),
        }



    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Make all fields required except 'product_discount'
        self.fields['product_discount'].required = False
        for h in self.fields.values():
            h.label = ''
