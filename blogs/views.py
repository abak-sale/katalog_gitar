from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.forms import inlineformset_factory # <-- Ditambahkan untuk handle FormSet Gambar
from .models import Category, Product, ProductImage # <-- Pastikan ProductImage diimpor di sini
from .forms import ProductForm,CategoryForm

# =========================================================================
# KONFIGURASI FORMSET: Digunakan bersama oleh halaman Tambah & Edit
# =========================================================================
ImageFormSet = inlineformset_factory(
    Product, 
    ProductImage,       # Mengaitkan tabel Product dengan tabel Gambar
    fields=['image'],   # Field nama file gambar di model Anda
    extra=10,           # Menampilkan 10 slot kosong langsung di halaman depan
    can_delete=True     # Mengaktifkan fitur hapus foto (khusus saat edit produk)
)


# =========================================================================
# 1. HALAMAN UTAMA / KATALOG
# =========================================================================
class ProductListView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.all()
        
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('q', '')
        return context


# =========================================================================
# 2. HALAMAN DETAIL PRODUK
# =========================================================================
class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


# =========================================================================
# 3. HALAMAN TAMBAH PRODUK (Locked + FormSet 10 Gambar)
# =========================================================================
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_new.html"
    success_url = reverse_lazy("home")
    login_url = "login" 

    # Menyisipkan 10 slot gambar kosong ke form tambah
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ImageFormSet()
        return context

    # Menyimpan data produk dan 10 gambarnya sekaligus
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        if form.is_valid() and image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


# =========================================================================
# 4. HALAMAN EDIT PRODUK (Locked + Load Data Gambar Lama & Fitur Hapus)
# =========================================================================
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_edit.html"
    success_url = reverse_lazy("home")
    login_url = "login"

    # Memuat data teks beserta gambar-gambar yang sudah tersimpan sebelumnya
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(
                self.request.POST, 
                self.request.FILES, 
                instance=self.object
            )
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
        return context

    # Menyimpan perubahan teks, foto baru, atau foto yang dicentang hapus
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        if form.is_valid() and image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


# =========================================================================
# 5. HALAMAN KONFIRMASI HAPUS PRODUK (Locked)
# =========================================================================
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product_delete.html"
    success_url = reverse_lazy("home")
    login_url = "login"
    
# =========================================================================
# 6. HALAMAN TAMBAH KATEGORI BARU (Locked)
# =========================================================================
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_new.html"
    success_url = reverse_lazy("product_new") # Setelah sukses simpan, otomatis balik ke halaman input produk
    login_url = "login"
    
    # TAMBAHKAN FUNGSI INI:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all() # Mengambil semua list kategori untuk ditampilkan di bawah form
        return context
    
# =========================================================================
# 7. HALAMAN EDIT KATEGORI (Locked)
# =========================================================================
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_edit.html"
    success_url = reverse_lazy("product_new") # Setelah diedit, balik ke halaman tambah produk
    login_url = "login"

# =========================================================================
# 8. HALAMAN HAPUS KATEGORI (Locked)
# =========================================================================
class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "category_delete.html"
    success_url = reverse_lazy("product_new")
    login_url = "login"
    
    