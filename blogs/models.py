import os
from django.db import models
from PIL import Image, ImageOps # <-- 1. IMPOR PUSTAKA PILLOW DI SINI

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
    image = models.ImageField(upload_to="products/", verbose_name="Foto Produk") # <-- Tetap pakai upload_to bawaanmu

    def __str__(self):
        return f"Foto untuk {self.product.title}"

    # =========================================================================
    # FITUR BARU: OPTIMASI & KOMPRESI GAMBAR OTOMATIS SEBELUM DISIMPAN
    # =========================================================================
    def save(self, *args, **kwargs):
        # 1. Jalankan fungsi save bawaan dulu agar file terunggah ke dalam folder media
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            
            # Memastikan file fisik gambarnya benar-benar ada sebelum dimodifikasi
            if os.path.exists(img_path):
                img = Image.open(img_path)

                # A. Auto-Rotate: Memperbaiki posisi foto jika terbalik/miring saat diambil pakai HP
                img = ImageOps.exif_transpose(img)

                # B. Batasi resolusi maksimal ke lebar/tinggi 1024px (Sudah sangat tajam untuk web)
                max_size = (1024, 1024)
                if img.height > 1024 or img.width > 1024:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # C. Ubah mode warna ke RGB jika gambarnya berformat PNG transparan agar bisa di-convert
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # D. Simpan ulang file dengan kompresi kualitas 80% (Ukuran drop drastis, detail tetap jernih)
                img.save(img_path, "JPEG", quality=80, optimize=True)
    # =========================================================================