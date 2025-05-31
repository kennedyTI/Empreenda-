# utils/verificar_mongodb.py

import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Obtém a URI do MongoDB do ambiente, ou usa o padrão para o serviço docker 'mongodb'
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")

def verificar_conexao_mongodb():
    """
    Verifica se é possível estabelecer conexão com o MongoDB.
    Exibe mensagem no log em caso de sucesso ou falha.
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        client.server_info()  # Força tentativa de conexão imediata
        logging.info("✅ Conexão com o MongoDB estabelecida com sucesso.")
    except ConnectionFailure as e:
        logging.error(f"❌ Falha ao conectar ao MongoDB: {e}")
