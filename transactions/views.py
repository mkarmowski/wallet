from django.shortcuts import render, get_object_or_404
from .models import Transaction, Category, Wallet


def transaction_detail(request, id):
    transaction = get_object_or_404(Transaction, pk=id)
    return render(request, 'transaction/detail.html', {'transaction': transaction})


def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction/list.html', {'transactions': transactions})


def wallet_list(request):
    wallets = Wallet.objects.all()
    return render(request, 'transaction/list.html', {'wallets': wallets})


def wallet_detail(request, id):
    wallet = get_object_or_404(Wallet, pk=id)
    return render(request, 'transaction/detail.html', {'wallet': wallet})