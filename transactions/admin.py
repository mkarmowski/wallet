from django.contrib import admin
from .models import Category, Transaction


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name',]
admin.site.register(Category, CategoryAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'created',
                    'updated', 'amount']
    list_filter = ['name', 'category', 'created']
admin.site.register(Transaction, TransactionAdmin)