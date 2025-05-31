import subprocess
import os
from pathlib import Path

def atualizar_requirements():
    """
    Atualiza o arquivo requirements.txt com os pacotes atualmente instalados no ambiente,
    salvando sempre no diretório raiz do projeto (backend/requirements.txt).
    """
    try:
        # Caminho absoluto até o diretório raiz do projeto
        raiz = Path(__file__).resolve().parent.parent.parent
        caminho_reqs = raiz / "requirements.txt"

        with open(caminho_reqs, "w") as f:
            subprocess.run(["pip", "freeze"], stdout=f, check=True)

        print(f"[✓] requirements.txt atualizado em: {caminho_reqs}")
    except Exception as e:
        print(f"[✗] Erro ao atualizar requirements.txt: {e}")