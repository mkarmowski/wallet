from django.shortcuts import render, get_object_or_404
from .models import Transaction, Category


def transaction_detail(request, id):
    transaction = get_object_or_404(Transaction, pk=id)
    return render(request, 'transaction/detail.html', {'transaction': transaction})


def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction/list.html', {'transactions': transactions})
