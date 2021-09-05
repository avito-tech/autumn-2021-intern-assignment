from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["email", "is_staff", "is_active"]
    list_filter = ["email", "is_staff", "is_active"]
    fieldsets = (
        (_("Авторизация"), {'fields': ('email', 'password')}),
        (_("Персональная информация"), {
         'fields': ('first_name', 'last_name', 'phone', )}),
        (_("Разрешения"), {
         'fields': ('is_staff', 'is_active', 'is_superuser', )}),
        (_("Дополнительная информация"), {
         'fields': ('last_login', 'date_joined',)}),

    )
    add_fieldsets = (
        (None,
         {
             "classes": ("wide",),
             'fields': (
                 'email',
                 'password1',
                 'password2',
                 'is_staff',
                 'is_active'
             )
         }),
    )
    search_fields = ['email']


admin.site.register(User, UserAdmin)
