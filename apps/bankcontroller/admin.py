from django.contrib import admin

from .models import MoneyCard, Service, ShopService, Wallet

admin.site.register(Wallet)
admin.site.register(MoneyCard)
admin.site.register(Service)
admin.site.register(ShopService)
