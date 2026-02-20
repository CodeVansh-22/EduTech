from pymongo import MongoClient
from config import Config

# Initialize MongoDB client
client = MongoClient(Config.MONGO_URI)

# Create/Connect to the 'edutech_db' database
db = client.edutech_db

# Define collections for easy access
users_collection = db.users
courses_collection = db.courses
enrollments_collection = db.enrollments