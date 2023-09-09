import json
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from MainServer.database.totalAndLabel import *


@csrf_exempt
def addLabelController(request, u_id):
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            labelName = body.get("labelName")
            if addLabel(u_id=u_id, labelName=labelName):
                return HttpResponse(json.dumps({"msg": "Lable added"}), content_type='application/json')
            return HttpResponse(json.dumps({"msg": "Lable not added"}), content_type='application/json')
        else:
            return HttpResponseBadRequest(json.dumps({"msg": "bad Request"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')


@csrf_exempt
def deleteLabelController(request, u_id, labelId):
    try:
        if request.method == 'DELETE':
            if deleteLabel(doc_id=u_id, labelId=labelId):
                return HttpResponse(json.dumps({"msg": "Lable deleted"}), content_type='application/json')
            return HttpResponse(json.dumps({"msg": "Lable not deleted"}), content_type='application/json')
        else:
            return HttpResponseBadRequest(json.dumps({"msg": "bad Request"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')


@csrf_exempt
def editLabelController(request, u_id, labelId):
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            newLabel = body.get("newLabel")
            if  editLabelName(_id=u_id, labelId=labelId, newLabel=newLabel):
                return HttpResponse(json.dumps({"msg": "Lable edited"}), content_type='application/json')
            return HttpResponse(json.dumps({"msg": "Lable not edited"}), content_type='application/json')
        else:
            return HttpResponseBadRequest(json.dumps({"msg": "bad Request"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')


@csrf_exempt
def changeDefaultLabelController(request, u_id, labelId):
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            oldDefaultLableId = (body.get("oldDefaultLableId"))
            if setDefaultLabel(_id=u_id, labelId=labelId, oldDefaultLableId=oldDefaultLableId):
                return HttpResponse(json.dumps({"msg": "default Lable changed"}), content_type='application/json')
            return HttpResponse(json.dumps({"msg": "default Lable not changed"}), content_type='application/json')
        else:
            return HttpResponseBadRequest(json.dumps({"msg": "bad Request"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')


@csrf_exempt
def getLabelsController(request, u_id):
    try:
        if request.method == 'GET':
            return HttpResponse(json.dumps({"labels": getLabels(u_id)}), content_type='application/json')
        else:
            return HttpResponseBadRequest(json.dumps({"msg": "bad Request"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')
