from pymongo import MongoClient
from backend.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.finance_guardian

users_collection = db.users
expenses_collection = db.expenses
goals_collection = db.goals
subscriptions_collection = db.subscriptions
alerts_collection = db.alerts
