from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^wallet/list/$', views.wallet_list, name='wallet_list'),
    url(r'^transaction/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.transaction_detail, name='transaction_detail'),
    url(r'^transaction/list/$', views.transaction_list, name='transactions_list'),
    url(r'^wallet/detail/(?P<id>\d+)/$', views.wallet_details, name='wallet_details'),
]
