from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^wallet/list/$', views.wallet_list, name='wallet_list'),
    url(r'^transaction/list/$', views.transaction_list, name='transactions_list'),
    url(r'^transaction/detail/(?P<id>\d+)/$', views.transaction_detail, name='transaction_details'),
    url(r'^wallet/detail/(?P<id>\d+)/$', views.wallet_details, name='wallet_details'),
    url(r'^wallet/create/$', views.wallet_create, name='wallet_create'),
    url(r'^transaction/create/$', views.transaction_create, name='transaction_create'),
]
