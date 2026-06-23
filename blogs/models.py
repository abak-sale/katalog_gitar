# FILE: blogs/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nama Kategori")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Kategori")
    title = models.CharField(max_length=200, verbose_name="Nama Produk")
    price = models.IntegerField(verbose_name="Harga (Rp)")
    description = models.TextField(verbose_name="Deskripsi Produk")
    created_at = models.DateTimeField(auto_now_add=True)

    # =========================================================================
    # FITUR BARU: PILIHAN STATUS STOK GITAR
    # =========================================================================
    STATUS_CHOICES = [
        ('ready', 'Ready Stock'),
        ('booked', 'Booked (Uang Muka)'),
        ('sold', 'Sold Out (Terjual)'),
    ]
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ready', # Setiap tambah produk baru, otomatis berstatus Ready
        verbose_name="Status Stok"
    )
    # =========================================================================

    def __str__(self):
        return self.title

    # Nanti kita akan arahkan redirect setelah input ke halaman detail produk
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={"pk": self.pk})


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/", verbose_name="Foto Produk")

    def __str__(self):
        return f"Foto untuk {self.product.title}"