
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from MainServer.home import *

urlpatterns = [
    path('', index, name="home"),
    path('expense/', include('MainServer.urls')),
    # path('expense/', include('MainServer.Routes.expense')),
    path('admin/', admin.site.urls),
]
