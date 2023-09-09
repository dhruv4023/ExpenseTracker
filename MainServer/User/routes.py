
from django.urls import path
from MainServer.User.controller import *
urlpatterns = [
    path('signup/', signUp, name="signUp"),
    path('login/', login, name="login"),
    # path('verifyOtp/', verifyOtp, name="verifyOtp"),
    # path('getcontact/', getContact, name="getcontact"),
    # path('delcontact/<str:id>/', delContact, name="delcontact"),
]

