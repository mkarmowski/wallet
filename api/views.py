from django.contrib.auth.models import User
from rest_framework import generics, mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from budgets.models import Budget, Saving
from transactions.models import Wallet, Category, Transaction
from .serializers import WalletSerializer, CategorySerializer, TransactionSerializer, \
    BudgetSerializer, SavingSerializer, UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('api:users_list', request=request, format=format),
        'wallets': reverse('api:wallet_list', request=request, format=format),
        'categories': reverse('api:category_list', request=request, format=format),
        'transactions': reverse('api:transaction_list', request=request, format=format),
        'budgets': reverse('api:budget_list', request=request, format=format),
        'savings': reverse('api:saving_list', request=request, format=format),
    })


class ListView(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DetailView(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserListView(ListView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(DetailView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class WalletListView(ListView):
    serializer_class = WalletSerializer

    def get_queryset(self):
            user = self.request.user
            return Wallet.objects.filter(user=user)


class WalletDetailView(DetailView):
    serializer_class = WalletSerializer

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(user=user)


class CategoryListView(ListView):
    serializer_class = CategorySerializer

    def get_queryset(self):
            user = self.request.user
            return Category.objects.filter(user=user)


class CategoryDetailView(DetailView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(user=user)


class TransactionListView(ListView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
            user = self.request.user
            return Transaction.objects.filter(user=user)


class TransactionDetailView(DetailView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)


class BudgetListView(ListView):
    serializer_class = BudgetSerializer

    def get_queryset(self):
            user = self.request.user
            return Budget.objects.filter(user=user)


class BudgetDetailView(DetailView):
    serializer_class = BudgetSerializer

    def get_queryset(self):
        user = self.request.user
        return Budget.objects.filter(user=user)


class SavingListView(ListView):
    serializer_class = SavingSerializer

    def get_queryset(self):
            user = self.request.user
            return Saving.objects.filter(user=user)


class SavingDetailView(DetailView):
    serializer_class = SavingSerializer

    def get_queryset(self):
        user = self.request.user
        return Saving.objects.filter(user=user)
