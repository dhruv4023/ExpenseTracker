from MainServer.database.uniqueId import *
from MainServer.database.mongodb import *
from MainServer.database.totalAndLabel import addNewTotalLabelDoc, incrementInTotalCollection, decrementInTotalCollection, decreamentAndIncrement
from MainServer.database.archived import archiveTransactions


# to add new document
def addTransMethod(userName: str, methodName: str, yyyy: str = str(datetime.now().date())[:4]):
    _id = userName+"_"+yyyy[2:]
    doc = {
        "_id": _id,
        "title": methodName,
        "year":  yyyy,
        "transactions": [],
        "startedOn": str(datetime.now()),
    }
    validate_document(document=doc, schema=transactionsMethodsSchema)
    transactionsMethods.insert_one(doc)
    res = addNewTotalLabelDoc(_id)
    return True and res


# to add new transaction to transactions array
def addNewTransaction(userId: str, comment: str, labelId: str, amt: int, dateTime: str = getDateTimeUniqueNumber()):
    transactionMethodId = userId+"_"+dateTime[:2]
    doc = {
        "_id": str(getUniqueId()),
        "dateTime": dateTime,
        "comment": comment,
        "labelId": labelId,
        "amt": amt,
    }
    validate_document(document=doc, schema=transactionSchema)
    query = {"_id": transactionMethodId}
    update = {
        "$push": {"transactions": {"$each": [doc], "$position": 0}},
    }

    if transactionsMethods.count_documents(query, limit=1) == 1:
        try:
            return incrementInTotalCollection(transactionMethodId, doc) and updateOne(query, update) != 0
        except:
            return decrementInTotalCollection(transactionMethodId, doc)
    else:
        addTransMethod(userName=userId, methodName=users.find_one(
            {"_id": userId})["name"]+"'s Transactions")
        archiveTransactions(doc_id=transactionMethodId)
        return addNewTransaction(userId=userId, comment=comment, labelId=labelId, amt=amt, dateTime=dateTime)


# to delete a transaction from transactions array
def deleteTransaction(transactionMethodId: str, trasactionData: dict):
    query = {"_id": transactionMethodId}
    update = {
        "$pull": {
            "transactions": {
                "_id": trasactionData["transactionId"]
            }
        }
    }
    try:
        return decrementInTotalCollection(transactionMethodId, trasactionData) and updateOne(query, update)
    except:
        return incrementInTotalCollection(transactionMethodId, trasactionData)


# to edit comment in a transaction
def editTransactionsComment(transactionMethodId: str, transactionId: str, comment: str):
    query = {
        "_id": transactionMethodId,
        "transactions._id": transactionId
    }
    update = {
        "$set": {
            "transactions.$.comment": comment
        }
    }
    return updateOne(query, update)


# to edit label in a transaction
def changelableTransactions(transactionMethodId: str, newLabelId: str, trasactionData: dict):
    query = {
        "_id": transactionMethodId,
        "transactions._id": trasactionData["transactionId"]
    }
    update = {
        "$set": {
            "transactions.$.labelId": newLabelId
        }
    }

    try:
        decreamentAndIncrement(doc_id=transactionMethodId,
                               newLabelId=newLabelId, trasactionData=trasactionData)
        newLabelId, trasactionData["labelId"] = trasactionData["labelId"], newLabelId
        if 0 == updateOne(query, update):
            decreamentAndIncrement(
                doc_id=transactionMethodId, newLabelId=newLabelId, trasactionData=trasactionData)
        return True
    except:
        return decreamentAndIncrement(doc_id=transactionMethodId,
                                      newLabelId=newLabelId, trasactionData=trasactionData)


# to retrive transactions
def getTransactions(transactionMethodId: str, startIndex: int = 0, limit: int = 10):
    query = {"_id": transactionMethodId}
    return transactionsMethods.find(query, {"transactions": {"$slice": [startIndex, limit]}})


# common updateOne function
def updateOne(query, update):
    return transactionsMethods.update_one(query, update).modified_count
