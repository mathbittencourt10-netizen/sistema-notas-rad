from typing import Optional
from config.settings import USUARIOS


class AuthController:
    """Responsável pela autenticação de usuários."""

    def autenticar(self, username: str, senha: str) -> Optional[dict]:
        """Valida credenciais e retorna dados do usuário ou None."""
        if username in USUARIOS and USUARIOS[username]["senha"] == senha:
            dados = USUARIOS[username]
            return {"username": username, "nome": dados["nome"], "tipo": dados["tipo"]}
        return None
