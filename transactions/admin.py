from django.contrib import admin

from .models import Category, Transaction, Wallet


class WalletAdmin(admin.ModelAdmin):
    list_display = ['name', 'balance', 'user']
    list_filter = ['name', ]
admin.site.register(Wallet, WalletAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', ]
    list_filter = ['name', 'user', ]
admin.site.register(Category, CategoryAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created',
                    'updated', 'amount', 'wallet']
    list_filter = ['name', 'category', 'created']
admin.site.register(Transaction, TransactionAdmin)
