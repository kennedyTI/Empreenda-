# Verifica conexão com o MongoDB no início do app

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
import os

# URI do MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")

# Função de verificação
def verificar_conexao_mongodb():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        client.server_info()
        logging.info("✅ Conexão com o MongoDB estabelecida com sucesso.")
    except ConnectionFailure as e:
        logging.error(f"❌ Falha ao conectar ao MongoDB: {e}")
