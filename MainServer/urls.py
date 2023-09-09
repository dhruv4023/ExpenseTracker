
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from MainServer.home import *

urlpatterns = [
    path('user/', include('MainServer.User.routes')),
    path('transactionmethod/', include('MainServer.TransactionMethod.routes')),
    path('mail/', include('MainServer.Mail.routes')),
    path('label/', include('MainServer.Label.routes')),
]
