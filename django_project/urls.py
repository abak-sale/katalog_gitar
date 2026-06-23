# FILE: django_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # <-- Impor settings proyek
from django.conf.urls.static import static # <-- Impor helper untuk file statis/media

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("blogs.urls")),
]

# Tambahkan baris ini di bawah URLpatterns utama:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)