from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^wallets/$', views.WalletListView.as_view(), name='wallet_list'),
    url(r'^wallets/(?P<pk>\d+)/$', views.WalletDetailView.as_view(), name='wallet_details'),
    url(r'^categories/$', views.CategoryListView.as_view(), name='category_list'),
    url(r'^categories/(?P<pk>\d+)/$', views.CategoryDetailView.as_view(), name='category_details'),
    url(r'^transactions/$', views.TransactionListView.as_view(), name='transaction_list'),
    url(r'^transactions/(?P<pk>\d+)/$', views.TransactionDetailView.as_view(), name='transaction_details'),
    url(r'^budgets/$', views.BudgetListView.as_view(), name='budget_list'),
    url(r'^budgets/(?P<pk>\d+)/$', views.BudgetDetailView.as_view(), name='budget_details'),
    url(r'^savings/$', views.SavingListView.as_view(), name='saving_list'),
    url(r'^savings/(?P<pk>\d+)/$', views.SavingDetailView.as_view(), name='saving_details'),
]
