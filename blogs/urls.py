from django.urls import path
from .views import (
    ProductListView, 
    ProductDetailView, 
    ProductCreateView,
    ProductUpdateView, # <-- Impor ini
    ProductDeleteView,  # <-- Impor ini
    CategoryCreateView,# <-- Impor class baru ini
    CategoryUpdateView, # <-- Impor ini
    CategoryDeleteView
)

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/new/", ProductCreateView.as_view(), name="product_new"),
    
    # Path BARU untuk Edit dan Hapus
    path("product/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    # PATH BARU: Akses tambah kategori halaman web
    path("category/new/", CategoryCreateView.as_view(), name="category_new"),
    # PATH BARU UNTUK EDIT & HAPUS KATEGORI (Menggunakan ID Kategori / <int:pk>)
    path("category/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_edit"),
    path("category/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),
]