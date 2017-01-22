import csv
import xlwt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, UpdateView

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from budgets.models import Budget
from transactions.filters import TransactionFilter
from .forms import WalletCreateForm, TransactionCreateForm, CategoryCreateForm
from .models import Transaction, Category, Wallet


@login_required
def wallet_list(request):
    current_user = request.user
    wallets = Wallet.objects.filter(user=current_user)
    return render(request, 'wallet/list.html', {'wallets': wallets})


@login_required
def wallet_details(request, id):
    user = request.user
    wallet = get_object_or_404(Wallet, id=id)
    transactions = Transaction.objects.filter(wallet=wallet)
    return render(request, 'wallet/detail.html', {'wallet': wallet,
                                                  'transactions': transactions})


@login_required
def wallet_create(request):
    if request.method == 'POST':
        wallet_create_form = WalletCreateForm(request.POST)
        if wallet_create_form.is_valid():
            new_wallet = wallet_create_form.save(commit=False)
            new_wallet.user = request.user
            new_wallet.save()
            messages.success(request, 'Wallet created')
            return render(request, 'wallet/done.html')
    else:
        wallet_create_form = WalletCreateForm()
    return render(request, 'wallet/create.html', {'wallet_form': wallet_create_form})


class WalletDelete(DeleteView):
    model = Wallet
    template_name = 'wallet/wallet_confirm_delete.html'
    success_url = reverse_lazy('wallet:wallet_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WalletDelete, self).dispatch(*args, **kwargs)


class WalletUpdate(UpdateView):
    model = Wallet
    fields = ['name', 'balance', 'description']
    template_name = 'wallet/update.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WalletUpdate, self).dispatch(*args, **kwargs)


@login_required
def category_list(request):
    current_user = request.user
    categories = Category.objects.filter(user=current_user)
    return render(request, 'category/list.html', {'categories': categories})


@login_required
def category_details(request, id):
    user = request.user
    category = get_object_or_404(Category, id=id)
    transactions = Transaction.objects.filter(category=category)
    return render(request, 'category/detail.html', {'category': category,
                                                    'transactions': transactions})


@login_required
def category_create(request):
    user = request.user
    if request.method == 'POST':
        category_create_form = CategoryCreateForm(request.POST)
        if category_create_form.is_valid():
            new_category = category_create_form.save(commit=False)
            new_category.user = request.user
            new_category.save()
            messages.success(request, 'Category created')
            return render(request, 'category/done.html')
    else:
        category_create_form = CategoryCreateForm()
    return render(request, 'category/create.html', {'category_form': category_create_form})


class CategoryDelete(DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('wallet:category_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CategoryDelete, self).dispatch(*args, **kwargs)


class CategoryUpdate(UpdateView):
    model = Category
    template_name = 'category/update.html'
    form_class = CategoryCreateForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CategoryUpdate, self).dispatch(*args, **kwargs)


@login_required
def transaction_list(request):
    current_user = request.user
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    objects = Transaction.objects.filter(user=current_user)
    p = Paginator(objects, 10, request=request)
    transactions = p.page(page)
    return render(request, 'transaction/list.html',
                  {'transactions': transactions})


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
            new_transaction.user = current_user
            wallet = get_object_or_404(Wallet, name=new_transaction.wallet)
            new_transaction.wallet_balance_adjust(wallet, new_transaction)  # Adjust chosen wallet balance
            new_transaction.save()

            # assign budget if applicable:
            budgets = Budget.objects.filter(user=current_user)
            for budget in budgets:
                transactions = Transaction.objects.filter(
                    Q(date__gte=budget.date_from)
                    & Q(date__lte=budget.date_to)
                    & Q(category=budget.category))
                if budget.category == new_transaction.category and budget.active is True:
                    new_transaction.budget = budget
                    new_transaction.save()
                    completion = budget.budget_completion(transactions)

                # check if the budget has reached limit:
                    if completion >= 100:
                        budget.finished, budget.finishing = True, False
                        messages.info(request,
                                      'You have reached the limit of your budget {}'
                                      .format(budget.name))
                    elif completion >= 80:
                        budget.finishing = True
                        messages.info(request,
                                      'You are almost at the limit of your budget {}'
                                      .format(budget.name))
                    budget.completion = completion
                    budget.save()
            messages.success(request, 'Transaction created')
            return render(request, 'transaction/done.html')
    else:

        transaction_create_form = TransactionCreateForm(current_user)
    return render(request, 'transaction/create.html',
                  {'transaction_form': transaction_create_form})


class TransactionDelete(DeleteView):
    model = Transaction
    template_name = 'transaction/transaction_confirm_delete.html'
    success_url = reverse_lazy('wallet:transactions_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TransactionDelete, self).dispatch(*args, **kwargs)


class TransactionUpdate(UpdateView):
    model = Transaction
    fields = ['name', 'type', 'wallet', 'category', 'date', 'amount', 'notes']
    template_name = 'transaction/update.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TransactionUpdate, self).dispatch(*args, **kwargs)


def export_transactions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Type', 'Date', 'Wallet', 'Category', 'Amount', 'Notes'])

    transactions = Transaction.objects.filter(user=request.user).values_list(
        'name', 'type', 'date', 'wallet', 'category', 'amount', 'notes')
    for transaction in transactions:
        writer.writerow(transaction)
    return response


def export_transactions_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="transactions.xls"'

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Transactions')

    # first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Name', 'Type', 'Date', 'Wallet', 'Category', 'Amount', 'Notes', ]

    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num], font_style)

    # other rows
    font_style = xlwt.XFStyle()
    rows = Transaction.objects.filter(user=request.user).values_list(
        'name', 'type', 'date', 'wallet', 'category', 'amount', 'notes')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, row[col_num], font_style)

    workbook.save(response)
    return response


def transaction_filter(request):
    f = TransactionFilter(request.GET, queryset=Transaction.objects.filter(user=request.user))
    return render(request, 'transaction/filter.html', {'filter': f})
