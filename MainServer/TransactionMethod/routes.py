
from django.urls import path
from MainServer.TransactionMethod.controller import *


urlpatterns = [
    path('add/<str:u_id>', add_transactions, name="addTransactions"),
    path('delete/<str:u_id>', delete_transactions, name="deleteTransactions"),
    path('edit/<str:u_id>/<str:transactionId>', edit_transactions, name="editTransactions"),
    path('changelable/<str:u_id>', changelable_transactions, name="changelableTransactions"),
    path('get/<str:u_id>/<str:startIndex>', get_transactions, name="getTransactions"),
]


