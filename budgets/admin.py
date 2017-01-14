from django.contrib import admin
from .models import Budget


class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'wallet', 'category',
                    'amount', 'date_from', 'date_to', 'active']
    list_filter = ['name', 'date_from', 'date_to']
admin.site.register(Budget, BudgetAdmin)
