"""
Configuração de conexão com MongoDB (container ou cloud).
Lê exclusivamente do ambiente do container.
"""

from pymongo import MongoClient
import os
import logging

logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not MONGO_URI:
    raise EnvironmentError("❌ MONGO_URI não definida.")
if not MONGO_DB_NAME:
    raise EnvironmentError("❌ MONGO_DB_NAME não definida.")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
