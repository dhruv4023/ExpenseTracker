
from django.urls import path
from MainServer.Label.controller import *

urlpatterns = [
    path('add/<str:u_id>', addLabelController, name="addLabel"),
    path('delete/<str:u_id>/<str:labelId>', deleteLabelController, name="deleteLabel"),
    path('edit/<str:u_id>/<str:labelId>', editLabelController, name="editLabel"),
    path('changedefault/<str:u_id>/<str:labelId>', changeDefaultLabelController, name="changeDefaultLabel"),
    path('get/<str:u_id>', getLabelsController, name="getLabels"),
]

