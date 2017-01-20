from django.contrib import admin
from .models import Budget, Saving


class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'wallet', 'category',
                    'amount', 'date_from', 'date_to', 'active']
    list_filter = ['name', 'date_from', 'date_to']
admin.site.register(Budget, BudgetAdmin)


class SavingAdmin(admin.ModelAdmin):
    list_display = ['name', 'goal', 'current_amount', 'user', 'date_from', 'finished']
    list_filter = ['name', 'user', 'finished']
admin.site.register(Saving, SavingAdmin)
