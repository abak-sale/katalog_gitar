from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta): # <-- Pastikan ada .Meta di dalam kurung ini
        model = CustomUser
        fields = ("username", "email") # <-- Kolom yang mau dimunculkan saat daftar

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")