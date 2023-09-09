# schema for user collection
usersSchema = {
    "_id": str,
    "name": str,
    "email": str,
    "password": str,
}

# schema for transactionsMethods and archived collection
transactionsMethodsSchema = {
    "_id": str,
    "title": str,
    "year": str,
    "transactions": list,
    "startedOn": str
}

transactionSchema = {
    "_id": str,
    "dateTime": str,
    "comment": str,
    "labelId": str,
    "amt": int,
}

# schema for transactionsMethods collection
totalLabelSchema = {
    "_id": str,
    "labels": list,
}

labelSchema = {
    "_id": str,
    "labelName": str,
    "default": bool,
    "jan": dict,
    "feb": dict,
    "mar": dict,
    "apr": dict,
    "may": dict,
    "jun": dict,
    "jul": dict,
    "aug": dict,
    "sep": dict,
    "oct": dict,
    "nov": dict,
    "dec": dict
}

totalSchema = {
    "dr": int,
    "cr": int,
}


def validate_document(document, schema):
    for field, field_type in schema.items():
        if field not in document:
            raise ValueError(f"Missing field: {field}")
        if not isinstance(document[field], field_type):
            raise ValueError(
                f"Invalid field type for {field}. Expected: {field_type.__name__}, Actual: {type(document[field]).__name__}")
