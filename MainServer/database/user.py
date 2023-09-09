from MainServer.database.mongodb import *
from MainServer.database.transactionsMethods import addTransMethod

# signup
def addNewuser(_id: str, name: str, email: str, password: str):
    doc = {
        "_id": _id,
        "name": name,
        "email": email,
        "password": password,
    }
    validate_document(document=doc, schema=usersSchema)
    users.insert_one(doc)
    res = addTransMethod(_id, name+"'s Transactions")
    return True and res


# log in
def getUserDetails(_id: str, email: str):
    u = None
    if _id is not None:
        u = users.find_one({"_id": _id})
    elif email is not None:
        u = users.find_one({"email": email})
    else:
        return None
    return u
