from django.contrib.auth.models import User
from rest_framework import serializers

from budgets.models import Budget, Saving
from transactions.models import Wallet, Category, Transaction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedRelatedField(view_name='api:user_details', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='api:user_details', read_only=True)

    class Meta:
        model = Wallet
        fields = ('name', 'balance', 'user', 'description')


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='api:user_details', read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'user')


class BudgetSerializer(serializers.ModelSerializer):
    wallet = serializers.HyperlinkedRelatedField(view_name='api:wallet_details', read_only=True)
    category = serializers.HyperlinkedRelatedField(view_name='api:category_details', read_only=True)
    user = serializers.HyperlinkedRelatedField(view_name='api:user_details', read_only=True)

    class Meta:
        model = Budget
        fields = ('name', 'amount', 'user', 'wallet', 'category',
                  'date_from', 'date_to', 'finished', 'completion')


class SavingSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='api:user_details', read_only=True)

    class Meta:
        model = Saving
        fields = ('name', 'goal', 'current_amount', 'user', 'finished')


class TransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.HyperlinkedRelatedField(view_name='api:wallet_details', read_only=True)
    category = serializers.HyperlinkedRelatedField(view_name='api:category_details', read_only=True)
    user = serializers.HyperlinkedRelatedField(view_name='api:user_details', read_only=True)
    budget = serializers.HyperlinkedRelatedField(view_name='api:budget_details', read_only=True)
    saving = serializers.HyperlinkedRelatedField(view_name='api:saving_details', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'name', 'type', 'user', 'wallet', 'category',
                  'budget', 'saving', 'date', 'amount', 'notes')
