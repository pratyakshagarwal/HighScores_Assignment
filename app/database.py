import logging
import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME: str = os.getenv("DB_NAME", "adaptive_test")

try:
    client: MongoClient = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    logger.info("MongoDB connected successfully.")
except ConnectionFailure as e:
    logger.critical(f"MongoDB connection failed: {e}")
    sys.exit(1)
except ConfigurationError as e:
    logger.critical(f"MongoDB configuration error: {e}")
    sys.exit(1)

db = client[DB_NAME]
questions_collection = db["questions"]
sessions_collection = db["sessions"]