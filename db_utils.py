# db_utils.py
from pymongo import MongoClient
import streamlit as st  # Only if you plan to use st.secrets for configuration

# Retrieve MongoDB URI from Streamlit secrets for security (optional)
MONGO_URI = st.secrets["mongo"]["uri"]

# Establish connection to the MongoDB Atlas cluster with increased timeout settings
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5000ms = 5 seconds

# Select your database and collection
db = client.myDatabase        # Use your actual database name
collection = db.metrics       # Use a collection named 'metrics'

def init_counter():
    """Initialize the counter document if it doesn't exist."""
    if collection.count_documents({"_id": "visit_count"}) == 0:
        collection.insert_one({"_id": "visit_count", "count": 0})

def update_visit_count():
    """Atomically increment the count and return the new value."""
    result = collection.find_one_and_update(
        {"_id": "visit_count"},
        {"$inc": {"count": 1}},
        return_document=True  # Ensures we get the updated document back
    )
    return result["count"]
