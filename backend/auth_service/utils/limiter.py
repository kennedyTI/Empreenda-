from time import time
from fastapi import HTTPException
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

# Dicionário que controla os acessos por IP (temporário e sem persistência)
tentativas_por_ip = {}

# Limite de tentativas por IP e intervalo em segundos
LIMITE_POR_IP = 3
INTERVALO_SEGUNDOS = 10  # Ex: máximo 3 requisições a cada 10 segundos por IP

def verificar_limite_ip(ip: str):
    """
    Verifica se o IP excedeu o número de tentativas permitidas no intervalo.
    Se exceder, levanta um erro HTTP 429 (Too Many Requests).
    """
    agora = time()

    # Inicializa lista de tentativas se for o primeiro acesso
    if ip not in tentativas_por_ip:
        tentativas_por_ip[ip] = []

    # Remove tentativas que passaram do intervalo
    tentativas_por_ip[ip] = [
        t for t in tentativas_por_ip[ip] if agora - t < INTERVALO_SEGUNDOS
    ]

    if len(tentativas_por_ip[ip]) >= LIMITE_POR_IP:
        print(f"[!] Tentativa de SPAM bloqueada para IP: {ip}")
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas. Tente novamente mais tarde."
        )

    # Registra nova tentativa
    tentativas_por_ip[ip].append(agora)
    print(f"[✓] IP permitido: {ip}")

def reset_spam_control():
    """Limpa os registros de tentativas para testes."""
    tentativas_por_ip.clear()
