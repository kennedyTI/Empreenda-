"""
Internacionalização de mensagens (i18n) para suporte multilíngue na API.
Atualmente suporta "pt" (português) e "en" (inglês).
"""

from typing import Literal

# 🔤 Tipo que restringe os valores válidos para idioma
IdiomaSuportado = Literal["pt", "en"]

# 🌍 Dicionário centralizado com mensagens em dois idiomas
MENSAGENS = {
    "signup.success": {
        "pt": "Usuário criado com sucesso",
        "en": "User successfully created"
    },
    "signup.error": {
        "pt": "Erro ao cadastrar usuário",
        "en": "Failed to create user"
    },
    "email_ja_cadastrado": {
        "pt": "E-mail já cadastrado",
        "en": "Email already registered"
    },
    "email_invalido": {
        "pt": "E-mail inválido",
        "en": "Invalid email address"
    },
    "senhas_diferentes": {
        "pt": "As senhas não conferem.",
        "en": "Passwords do not match."
    },
    "muitas_tentativas": {
        "pt": "Muitas tentativas. Tente novamente mais tarde.",
        "en": "Too many attempts. Try again later."
    },
    "rota_protegida": {
        "pt": "Você acessou uma rota protegida!",
        "en": "You accessed a protected route!"
    },
    "token_invalido": {
        "pt": "Token inválido ou expirado",
        "en": "Invalid or expired token"
    }
}

def traduzir(chave: str, lang: str = "pt") -> str:
    """
    Retorna a mensagem traduzida com base na chave e idioma fornecidos.

    Args:
    - chave (str): identificador da mensagem.
    - lang (str): idioma desejado ('pt' ou 'en').

    Returns:
    - Mensagem traduzida. Se chave ou idioma não encontrado, retorna a própria chave.
    """
    mensagem = MENSAGENS.get(chave)
    if mensagem:
        return mensagem.get(lang, mensagem.get("pt", chave))
    return chave  # 🔁 Fallback: retorna a chave literal se não existir
