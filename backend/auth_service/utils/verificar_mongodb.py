"""
Verifica a conexão com o MongoDB na inicialização do app.
Requisito crítico para funcionamento da API.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
import os

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise EnvironmentError("❌ MONGO_URI não definida no ambiente.")

def verificar_conexao_mongodb():
    """
    Tenta conectar ao MongoDB e exibe log de sucesso ou erro.
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        client.server_info()  # Força conexão
        logging.info("✅ Conexão com o MongoDB estabelecida com sucesso.")
    except ConnectionFailure as e:
        logging.error(f"❌ Falha ao conectar ao MongoDB: {e}")
        raise
