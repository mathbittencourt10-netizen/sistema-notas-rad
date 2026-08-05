from dataclasses import dataclass
from typing import Optional

@dataclass
class Aluno:
    """Representa um aluno com suas notas."""
    nome: str
    nota1: float
    nota2: float
    media: Optional[float] = None
    situacao: Optional[str] = None
