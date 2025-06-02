# backend/auth_service/db/mongo.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")  # Agora carrega corretamente do .env

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
