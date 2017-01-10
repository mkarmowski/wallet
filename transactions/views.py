from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import WalletCreateForm, TransactionCreateForm, CategoryCreateForm
from .models import Transaction, Category, Wallet


@login_required
def transaction_list(request):
    current_user = request.user
    transactions = Transaction.objects.filter(user=current_user)
    return render(request, 'transaction/list.html', {'transactions': transactions})


@login_required
def transaction_detail(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    return render(request, 'transaction/detail.html', {'transaction': transaction})



@login_required
def transaction_create(request):
    current_user = request.user
    if request.method == 'POST':
        transaction_create_form = TransactionCreateForm(current_user, request.POST)
        if transaction_create_form.is_valid():
            new_transaction = transaction_create_form.save(commit=False)
            new_transaction.user = request.user
            new_transaction.wallet = transaction_create_form.cleaned_data['wallet']
            new_transaction.save()
            return render(request, 'transaction/done.html')
    else:

        transaction_create_form = TransactionCreateForm(current_user)
    return render(request, 'transaction/create.html',
                  {'transaction_form': transaction_create_form})


@login_required
def wallet_list(request):
    current_user = request.user
    wallets = Wallet.objects.filter(user=current_user)
    return render(request, 'wallet/list.html', {'wallets': wallets})


@login_required
def wallet_details(request, id):
    user = request.user
    wallet = get_object_or_404(Wallet, id=id)
    return render(request, 'wallet/detail.html', {'wallet': wallet})


@login_required
def wallet_create(request):
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


@login_required
def category_list(request):
    current_user = request.user
    categories = Category.objects.filter(user=current_user)
    return render(request, 'category/list.html', {'categories': categories})


@login_required
def category_details(request, id):
    user = request.user
    category = get_object_or_404(Category, id=id)
    return render(request, 'category/detail.html', {'category': category})


@login_required
def category_create(request):
    user = request.user
    if request.method == 'POST':
        category_create_form = CategoryCreateForm(request.POST)
        if category_create_form.is_valid():
            new_category = category_create_form.save(commit=False)
            new_category.user = request.user
            new_category.save()
            return render(request, 'category/done.html')
    else:
        category_create_form = CategoryCreateForm()
    return render(request, 'category/create.html', {'category_form': category_create_form})



