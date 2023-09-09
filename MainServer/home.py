from django.shortcuts import render
from django.http import *
import json
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings


@csrf_exempt
def index(request):
    # return render(request, 'index.html')
    return HttpResponse("Server is running")