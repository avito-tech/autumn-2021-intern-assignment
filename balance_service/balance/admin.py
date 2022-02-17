from django.contrib import admin

from balance.models import Balance, Transaction, Transfer


class BalanceAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'amount',
        'owner',
        'created'
    )
    search_fields = ('owner',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'operation',
        'details',
        'sum',
        'created'
    )
    search_fields = ('user', 'operation')


class TransferAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'outcoming_id',
        'incoming_id'
    )
    search_fields = ('outcoming', 'incoming')


admin.site.register(Balance, BalanceAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Transfer, TransferAdmin)