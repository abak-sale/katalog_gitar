from django import forms
from .models import Product, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; font-size: 14px;', 
                'placeholder': 'Masukkan nama kategori baru (misal: Efek Gitar)...'
            }),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Menentukan kolom form berdasarkan field di models.py Anda (Ditambahkan 'status')
        fields = ['category', 'title', 'price', 'description', 'status']
        
        # Memberikan dekorasi/styling inputan agar kotak form terlihat modern dan rapi
        widgets = {
            'category': forms.Select(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; font-size: 14px;'}),
            'title': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; font-size: 14px;', 'placeholder': 'Masukkan model/tipe gitar (misal: Fender Stratocaster)...'}),
            'price': forms.NumberInput(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; font-size: 14px;', 'placeholder': 'Contoh: 2500000'}),
            'description': forms.Textarea(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; height: 120px; font-size: 14px;', 'placeholder': 'Tuliskan detail spesifikasi, kelengkapan, dan kondisi seken produk...'}),
            # STYLING BARU: Drop-down pilihan status stok gitar
            'status': forms.Select(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; font-size: 14px; background-color: #fff;'}),
        }