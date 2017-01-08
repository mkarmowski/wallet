from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Transaction, Category, Wallet


@login_required
def transaction_detail(request, id):
    transaction = get_object_or_404(Transaction, pk=id)
    return render(request, 'transaction/detail.html', {'transaction': transaction})


@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction/list.html', {'transactions': transactions})


@login_required
def wallet_list(request):
    current_user = request.user
    wallets = Wallet.objects.filter(user=current_user)
    # wallets = Wallet.objects.all()
    return render(request, 'wallet/list.html', {'wallets': wallets})


@login_required
def wallet_details(request, id):
    user = request.user
    wallet = get_object_or_404(Wallet, id=id)
    return render(request, 'wallet/detail.html', {'wallet': wallet})
