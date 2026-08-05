from dataclasses import dataclass

@dataclass
class Usuario:
    """Representa um usuário autenticado no sistema."""
    username: str
    nome: str
    tipo: str  # 'professor' ou 'aluno'

    @property
    def is_professor(self) -> bool:
        return self.tipo == "professor"
