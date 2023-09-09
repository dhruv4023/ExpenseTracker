from MainServer.database.mongodb import *
from MainServer.database.uniqueId import getUniqueId


months = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]


# to add new Document in TotalAndLabel
def addNewTotalLabelDoc(_id: str):
    doc = {
        "_id": _id,
        "labels": []
    }
    totalAndLabel.insert_one(doc)
    res = addLabel(_id, "default", labelId="0", default=True)
    return True and res


# to add new Label object in TotalAndLabel Document
def addLabel(u_id: str, labelName: str, labelId=str(getUniqueId()), default=False):
    _id = u_id+"_"+str(datetime.now().date())[2:4]
    doc = {
        "_id": labelId,
        "labelName": labelName,
        "default": default
    }
    doc = generateArrayOfMonthlyTotal(doc)
    validate_document(doc, schema=labelSchema)
    res = totalAndLabel.update_one(
        {"_id": _id}, {"$push": {"labels": doc}}).modified_count
    return True and res != 0


# to remove Label object from TotalAndLabel Document
def deleteLabel(doc_id: str, labelId: str):
    query = {"_id": doc_id}
    if labelId == "0":
        return "you can't delete default label"
    args = {"labels": {"$elemMatch": {"_id": labelId}}}
    labelData = totalAndLabel.find_one(query, args)["labels"][0]
    for i in months:
        if (labelData[i]["dr"] != 0 or labelData[i]["cr"] != 0):
            return "you have marked some transactions with this label ! plz remove and try again"
    x = totalAndLabel.update_one({"_id": doc_id}, {
        "$pull": {
            "labels": {
                "_id": labelId
            }
        }
    })
    return 0 != (x.modified_count)


# to set Label object as default in TotalAndLabel Document
def setDefaultLabel(_id: str, labelId: str, oldDefaultLabelId: str):
    query = {
        "_id": _id, "labels._id": {"$in": [labelId, oldDefaultLabelId]}
    }
    update = {
        "$set": {
            f"labels.$[new].default": True,
            f"labels.$[old].default": False
        }
    }
    array_filters = [
        {"new._id": labelId},
        {"old._id": oldDefaultLabelId},
    ]
    return 0 != totalAndLabel.update_one(query, update, array_filters=array_filters).modified_count


# to edit Label name in object of label in TotalAndLabel Document
def editLabelName(_id: str, labelId: str, newLabelName: str):
    query = {
        "_id": _id,
        "labels._id": labelId
    }
    update = {
        "$set": {
            "labels.$.labelName": newLabelName
        }
    }
    return 0 != totalAndLabel.update_one(query, update).modified_count


def getLabels(_id: str):
    return totalAndLabel.find_one({"_id": _id})["labels"]

# increment total while adiing new transaction
def incrementInTotalCollection(doc_id: str, trasactionData: dict):
    amt = trasactionData["amt"]
    labelId = trasactionData["labelId"]
    mm = int(trasactionData["dateTime"][2:4])
    label = "dr" if amt < 0 else "cr"

    query = {"_id": doc_id, "labels._id": labelId}
    inc_field = {"labels.$."+months[mm-1]+"."+label: abs(amt)}

    return 0 != totalAndLabel.update_one(query, {"$inc": inc_field}).modified_count


# decrement total while delete a transaction
def decrementInTotalCollection(doc_id: str, trasactionData: dict):
    amt = trasactionData["amt"]
    labelId = trasactionData["labelId"]
    mm = int(trasactionData["dateTime"][2:4])
    label = "dr" if amt < 0 else "cr"

    query = {"_id": doc_id, "labels._id": labelId}
    dec_field = {"labels.$."+months[mm-1]+"."+label: -(abs(amt))}

    return 0 != totalAndLabel.update_one(query, {"$inc": dec_field}).modified_count


# change total while changing label of a transaction
def decreamentAndIncrement(doc_id: str, newLabelId: str, trasactionData: dict):
    amt = trasactionData["amt"]
    oldLabelId = trasactionData["labelId"]
    mm = int((trasactionData["dateTime"][2:4]))

    label = "dr" if amt < 0 else "cr"
    query = {"_id": doc_id, "labels._id": {"$in": [newLabelId, oldLabelId]}}
    update = {
        "$inc": {
            f"labels.$[old]."+months[mm-1]+"."+label: -(abs(amt)),
            f"labels.$[new]."+months[mm-1]+"."+label: (abs(amt)),
        }
    }
    array_filters = [
        {"old._id": oldLabelId},
        {"new._id": newLabelId}
    ]

    return 0 != totalAndLabel.update_one(query, update, array_filters=array_filters).modified_count


def generateArrayOfMonthlyTotal(res):
    doc = {
        "dr": 0,
        "cr": 0,
    }
    validate_document(doc, totalSchema)
    for i in range(0, 12):
        res[months[i]] = doc
    return res
