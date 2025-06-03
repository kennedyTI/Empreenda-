"""
Controle temporário de tentativas por IP (rate limiting).
⚠️ Apenas para ambiente de desenvolvimento/testes.
"""

from time import time
from fastapi import HTTPException
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

# ⚠️ Dicionário em memória para controle de requisições por IP
# Este controle é reiniciado a cada vez que o container sobe
tentativas_por_ip = {}

# 🎛️ Configurações do limiter
LIMITE_POR_IP = 3               # Máximo de 3 requisições...
INTERVALO_SEGUNDOS = 10         # ... a cada 10 segundos por IP

def verificar_limite_ip(ip: str):
    """
    Verifica se o IP excedeu o número de tentativas permitidas no intervalo.
    Se sim, levanta HTTP 429 (Too Many Requests).
    """
    agora = time()

    # Inicializa lista de tentativas se for a primeira vez
    if ip not in tentativas_por_ip:
        tentativas_por_ip[ip] = []

    # Remove entradas antigas fora do intervalo de tempo
    tentativas_por_ip[ip] = [
        t for t in tentativas_por_ip[ip] if agora - t < INTERVALO_SEGUNDOS
    ]

    if len(tentativas_por_ip[ip]) >= LIMITE_POR_IP:
        print(f"[!] Tentativa de SPAM bloqueada para IP: {ip}")
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas. Tente novamente mais tarde."
        )

    # Registra nova tentativa válida
    tentativas_por_ip[ip].append(agora)
    print(f"[✓] IP permitido: {ip}")

def reset_spam_control():
    """
    Limpa os registros de tentativas (usado apenas em testes automatizados).
    """
    tentativas_por_ip.clear()
