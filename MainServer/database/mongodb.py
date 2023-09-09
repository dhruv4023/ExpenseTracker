from MainServer.database.schemas import *
from datetime import datetime
from pymongo import MongoClient
import ssl
DB_URL = "mongodb://localhost:27017"

# adding not adding the security by Secure Socket Layer
client = MongoClient(DB_URL, ssl_cert_reqs=ssl.CERT_NONE)

DB_URL = "mongodb://localhost:27017"

print("connected successfully")

db = client["ExpenseTrackerDb"]

# all collections
users = db["users"]
transactionsMethods = db["transactionsMethods"]
totalAndLabel = db["totalAndLabel"]
archivedTransactions = db["archivedTransactions"]
archivedTotalAndLabel = db["archivedTotalAndLabel"]
