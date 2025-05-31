# backend/auth_service/db/mongo.py

from pymongo import MongoClient
import os

# Recupera URI do Mongo a partir de variável de ambiente (padrão: localhost)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
DB_NAME = "empreendadb"

# Cria conexão com o MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
