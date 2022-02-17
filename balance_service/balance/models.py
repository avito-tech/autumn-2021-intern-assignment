from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator


User = get_user_model()

OPERATIONS = [
    ('refill', 'refill'),
    ('withdraw', 'withdraw'),
    ('transfer', 'transfer')
]


class Balance(models.Model):
    
    amount = models.DecimalField(
        'Баланс пользователя',
        decimal_places=2,
        max_digits=10,
        default=0.00        
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='balance'
    )
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )


class Transaction(models.Model):
        
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='transactions'
    )
    operation = models.CharField(
        'Тип операции',
        max_length=30,
        choices=OPERATIONS
    )
    details = models.CharField('Детали операции', max_length=255)
    created = models.DateTimeField(
        'Дата совершения операции',
        auto_now_add=True
    )
    sum = models.DecimalField(
        'Сумма',
        decimal_places=2,
        max_digits=10,
        validators=(
            MinValueValidator(0.01, 'Требуется ввести сумму'),
        )
    )


class Transfer(models.Model):
    outcoming = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        verbose_name='Исходящий перевод',
        related_name='outcoming_transfer'
    )
    incoming = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        verbose_name='Входящий перевод',
        related_name='incoming_transfer'
    )