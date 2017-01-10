from django.contrib import admin
from .models import Category, Transaction, Wallet


class WalletAdmin(admin.ModelAdmin):
    list_display = ['name', 'balance', 'user']
    list_filter = ['name', ]
admin.site.register(Wallet, WalletAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name', ]

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'created',
                    'updated', 'amount', 'wallet']
    list_filter = ['name', 'category', 'created']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
admin.site.register(Transaction, TransactionAdmin)
