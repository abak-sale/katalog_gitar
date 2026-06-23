# FILE: blogs/admin.py
from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 10  # Menyediakan 10 slot upload foto langsung
    max_num = 10 # Maksimal 10 foto

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ["title", "category", "price", "created_at"]
    list_filter = ["category"]
    search_fields = ["title", "description"]

admin.site.register(Category)