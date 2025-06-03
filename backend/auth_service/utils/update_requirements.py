"""
Atualiza automaticamente o arquivo requirements.txt
⚠️ Deve ser usado apenas no ambiente de desenvolvimento (ENV=dev).
"""

import subprocess
import os
from pathlib import Path

def atualizar_requirements():
    """
    Executa pip freeze e sobrescreve requirements.txt com dependências atuais.
    """
    try:
        raiz = Path(__file__).resolve().parent.parent.parent
        caminho_reqs = raiz / "requirements.txt"

        with open(caminho_reqs, "w") as f:
            subprocess.run(["pip", "freeze"], stdout=f, check=True)

        print(f"[✓] requirements.txt atualizado em: {caminho_reqs}")
    except Exception as e:
        print(f"[✗] Erro ao atualizar requirements.txt: {e}")
