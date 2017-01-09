from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import WalletCreateForm
from .models import Transaction, Category, Wallet


@login_required
def transaction_list(request):
    current_user = request.user
    transactions = Transaction.objects.filter(user=current_user)
    # transactions = Transaction.objects.all ()
    return render(request, 'transaction/list.html', {'transactions': transactions})


@login_required
def transaction_detail(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    return render(request, 'transaction/detail.html', {'transaction': transaction})


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


@login_required
def wallet_create(request,):
    if request.method == 'POST':
        wallet_create_form = WalletCreateForm(request.POST)
        if wallet_create_form.is_valid():
            new_wallet = wallet_create_form.save(commit=False)
            new_wallet.user = request.user
            new_wallet.save()
            return render(request, 'wallet/done.html')
    else:
        wallet_create_form = WalletCreateForm()
    return render(request, 'wallet/create.html', {'wallet_form': wallet_create_form})
