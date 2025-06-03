"""
Schemas de entrada e saída para a rota /signup do serviço de autenticação.
Inclui validações completas para nome, e-mail, senha e confirmação de senha.
"""

from pydantic import BaseModel, Field, field_validator
from pydantic import model_validator  # Para validações de modelo no Pydantic v2
from email_validator import validate_email, EmailNotValidError

class SignupRequest(BaseModel):
    """
    Modelo para entrada de dados no cadastro de usuário (/signup).

    Validações:
    - Nome com no mínimo 2 caracteres
    - Senha com no mínimo 8 caracteres
    - Confirmação de senha
    - E-mail com verificação real
    """

    nome: str = Field(..., min_length=2, example="João Silva")
    email: str = Field(..., example="joao@exemplo.com")
    senha: str = Field(..., min_length=8, example="senhaSegura123")
    confirmar_senha: str = Field(..., min_length=8, example="senhaSegura123")

    @field_validator("email")
    def validar_email(cls, v):
        """
        Valida o e-mail com o pacote email-validator.
        Garante que seja um e-mail válido e formatado corretamente.
        """
        try:
            validate_email(v)
            return v
        except EmailNotValidError:
            raise ValueError("E-mail inválido")

    @model_validator(mode="after")
    def verificar_senhas_iguais(self) -> "SignupRequest":
        """
        Verifica se os campos 'senha' e 'confirmar_senha' são iguais.
        Executado após validação individual dos campos.
        """
        if self.senha != self.confirmar_senha:
            raise ValueError("As senhas não conferem.")
        return self

class SignupResponse(BaseModel):
    """
    Modelo de resposta da rota /signup.

    Exemplo de resposta:
    {
        "mensagem": "Usuário criado com sucesso!",
        "id": "6657f7f94f3ec40e1947aabc"
    }
    """
    mensagem: str
    id: str
