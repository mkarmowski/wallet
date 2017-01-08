from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^transactions/', include('transactions.urls')),
    url(r'^', include('users.urls')),
    url(r'^users/', include('users.urls')),

]
