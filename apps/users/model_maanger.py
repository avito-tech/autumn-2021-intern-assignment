from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    """Менеджер создания пользователя"""

    def email_valid(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_("Введите корректно email"))

    def create_user(self, email, password, **extra_fields):
        """Создание и сохранение пользователя комбинацией email-password"""
        if email:
            email = self.normalize_email(email)
            self.email_valid(email)
        else:
            raise ValidationError(_("Данный email уже используется"))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Создание суперпользователя комбинацией email-password"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValidationError(
                _("Суперпользователь должен иметь is_staff=True"))

        if extra_fields.get("is_superuser") is not True:
            raise ValidationError(
                _("Суперпользователь должен иметь is_superuser=True"))

        if email:
            email = self.normalize_email(email)
            self.email_valid(email)
        else:
            raise ValidationError(_("Данный email уже используется"))

        user = self.create_user(email, password, **extra_fields)
        return user
