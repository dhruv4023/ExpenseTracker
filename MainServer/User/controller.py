import json
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from MainServer.database.user import addNewuser, getUserDetails
from django.contrib.auth.hashers import make_password, check_password


@csrf_exempt
def signUp(request):
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            _id = body.get("_id")
            name = body.get('name')
            email = body.get('email')
            password = body.get('password')
            hashed_password = make_password(password)
            res = addNewuser(_id, name, email, hashed_password)
            # print(res)
            if res:
                return HttpResponse(json.dumps({"msg": "New user saved "}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"msg": "Failed to create user"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')


@csrf_exempt
def login(request):
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            _id = body.get("_id")
            email = body.get('email')
            password = body.get('password')
            userData = getUserDetails(_id, email)
            hashed_password = userData["password"]
            userData["password"]=None
            password_valid = check_password(password, hashed_password)
            if password_valid:
                return HttpResponse(json.dumps({"msg": "Log in success", "userData": userData}), content_type='application/json')
            return HttpResponse(json.dumps({"msg": "Invalid Credentials"}), content_type='application/json')
        else:
            return HttpResponseBadRequest(json.dumps({"msg": "bad Request"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')
