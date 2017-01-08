from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^transaction/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.transaction_detail, name='transaction_detail'),
    url(r'^list/$', views.transaction_list, name='transactions_list'),
]