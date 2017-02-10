from django.contrib.auth.models import User
from rest_framework import serializers

from budgets.models import Budget, Saving
from transactions.models import Wallet, Category, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('name', 'balance', 'user', 'description')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'user')


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('name', 'amount', 'user', 'wallet', 'category',
                  'date_from', 'date_to', 'finished', 'completion')


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = ('name', 'goal', 'current_amount', 'user', 'finished')


class TransactionSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()
    category = CategorySerializer()
    user = UserSerializer()
    budget = BudgetSerializer()
    saving = SavingSerializer()

    class Meta:
        model = Transaction
        fields = ('id', 'name', 'type', 'user', 'wallet', 'category',
                  'budget', 'saving', 'date', 'amount', 'notes')
