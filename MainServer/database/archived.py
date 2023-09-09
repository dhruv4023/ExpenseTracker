from MainServer.database.mongodb import *
from MainServer.database.totalAndLabel import addLabel


# to archive previous year transactions
def archiveTransactions(doc_id: str):
    # print(doc_id)
    oldTransMethId = doc_id[:-2]+str(int(doc_id[-2:])-1)
    oldIdQuery = {"_id": oldTransMethId}

    tranMethObj = transactionsMethods.find_one(oldIdQuery)
    totalAndLabelObj = totalAndLabel.find_one(oldIdQuery)

    # print(totalAndLabelObj)
    if archivedTransactions.insert_one(tranMethObj) and archivedTotalAndLabel.insert_one(totalAndLabelObj):
        transactionsMethods.delete_one(oldIdQuery)
        totalAndLabel.delete_one(oldIdQuery)

        try:
            labelNames = totalAndLabelObj["labels"]
            # print(labelNames)
            i = 0
            for label in labelNames:
                # print(label["labelName"])
                if i:
                    addLabel(_id=doc_id, labelName=label["labelName"])
                else:
                    i = 1
        except:
            print("label not added")

    return True
