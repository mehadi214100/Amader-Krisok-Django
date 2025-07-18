from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'product_name', 'price', 'image', 'stock', 'unit', 'is_available', 'location']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'পণ্যের নাম লিখুন'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'প্রতি কেজি/পিস দাম'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'মোট পরিমাণ'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'অবস্থান'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
            for field_name in self.fields:
                self.fields[field_name].required = True
