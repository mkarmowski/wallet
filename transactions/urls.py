from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^wallet/list/$', views.wallet_list, name='wallet_list'),
    url(r'^wallet/detail/(?P<id>\d+)/$', views.wallet_details, name='wallet_details'),
    url(r'^wallet/create/$', views.wallet_create, name='wallet_create'),
    url(r'^wallet/delete/(?P<pk>\d+)/$', views.WalletDelete.as_view(), name='wallet_delete'),
    url(r'^category/list/$', views.category_list, name='category_list'),
    url(r'^category/detail/(?P<id>\d+)/$', views.category_details, name='category_details'),
    url(r'^category/create/$', views.category_create, name='category_create'),
    url(r'^category/delete/(?P<pk>\d+)/$', views.CategoryDelete.as_view(), name='category_delete'),
    url(r'^transaction/list/$', views.transaction_list, name='transactions_list'),
    url(r'^transaction/detail/(?P<id>\d+)/$', views.transaction_detail, name='transaction_details'),
    url(r'^transaction/create/$', views.transaction_create, name='transaction_create'),
    url(r'^transaction/delete/(?P<pk>\d+)/$', views.TransactionDelete.as_view(), name='transaction_delete'),
]
