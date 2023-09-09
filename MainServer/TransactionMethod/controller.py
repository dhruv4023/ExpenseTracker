import json
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from MainServer.database.transactionsMethods import addNewTransaction, deleteTransaction, editTransactionsComment, changelableTransactions, getTransactions


@csrf_exempt
def add_transactions(request, u_id):
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            comment = body.get("comment")
            amt = body.get("amt")
            labelId = body.get("labelId")
            x = addNewTransaction(
                userId=u_id, comment=comment, amt=amt, labelId=labelId)
            # print(x)
            if x:
                return HttpResponse(json.dumps({"msg": "added"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"msg": "failed to add"}), content_type='application/json')
        else:
            return HttpResponseBadRequest(json.dumps({"msg": "bad Request"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')


@csrf_exempt
def delete_transactions(request, u_id):
    try:
        if request.method == 'DELETE':
            body = json.loads(request.body)
            trasactionData = body.get("transactiondata")
            if deleteTransaction(transactionMethodId=u_id, trasactionData=trasactionData):
                return HttpResponse(json.dumps({"msg": "deleted "+trasactionData["transactionId"]}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"msg": "failed to delete "+trasactionData["transactionId"]}), content_type='application/json')
        else:
            return HttpResponseBadRequest(json.dumps({"msg": "bad Request"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')


@csrf_exempt
def edit_transactions(request, u_id, transactionId):
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            if editTransactionsComment(transactionMethodId=u_id, transactionId=transactionId, comment=body.get("comment")):
                return HttpResponse(json.dumps({"msg": "comment edited"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"msg": "comment edit failed"}), content_type='application/json')
        else:
            return HttpResponseBadRequest(json.dumps({"msg": "bad Request"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')


@csrf_exempt
def changelable_transactions(request, u_id):
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            trasactionData = body.get("transactiondata")
            newLabelId = body.get("newLabelId")
            if changelableTransactions(transactionMethodId=u_id, newLabelId=newLabelId, trasactionData=trasactionData):
                return HttpResponse(json.dumps({"labels": "label changed"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"labels": "label change failed"}), content_type='application/json')
        else:
            return HttpResponseBadRequest(json.dumps({"msg": "bad Request"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')


@csrf_exempt
def get_transactions(request, u_id, startIndex):
    try:
        if request.method == 'GET':
            return HttpResponse(json.dumps({"transactions": getTransactions(transactionMethodId=u_id, startIndex=startIndex)}), content_type='application/json')
        else:
            return HttpResponseBadRequest(json.dumps({"msg": "bad Request"}), content_type='application/json')

    except:
        return HttpResponseServerError(json.dumps({"msg": "Server Error"}), content_type='application/json')
