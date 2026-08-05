import os
import pandas as pd
from models.aluno import Aluno
from config.settings import ARQUIVO_DADOS, COLUNAS, NOTA_APROVACAO, NOTA_RECUPERACAO


class NotaController:
    """Responsável pelo CRUD de notas usando pandas e Excel."""

    def __init__(self):
        self.arquivo = ARQUIVO_DADOS

    # ── Utilitários ────────────────────────────────────────────────────────
    def calcular_situacao(self, nota1: float, nota2: float) -> tuple:
        """Calcula a média e retorna (media, situacao)."""
        media = round((nota1 + nota2) / 2, 2)
        if media >= NOTA_APROVACAO:
            situacao = "Aprovado"
        elif media >= NOTA_RECUPERACAO:
            situacao = "Em Recuperação"
        else:
            situacao = "Reprovado"
        return media, situacao

    def _carregar(self) -> pd.DataFrame:
        """Carrega os dados do arquivo Excel."""
        if os.path.exists(self.arquivo):
            return pd.read_excel(self.arquivo)
        return pd.DataFrame(columns=COLUNAS)

    def _salvar(self, df: pd.DataFrame) -> None:
        """Salva os dados no arquivo Excel."""
        df.to_excel(self.arquivo, index=False, engine="openpyxl")

    # ── Consultas ──────────────────────────────────────────────────────────
    def listar_todos(self) -> list:
        return self._carregar().to_dict("records")

    def buscar_por_nome(self, texto: str) -> list:
        df = self._carregar()
        return df[df["Aluno"].str.contains(texto, case=False, na=False)].to_dict("records")

    def obter_dados_aluno(self, nome: str) -> list:
        df = self._carregar()
        return df[df["Aluno"] == nome].to_dict("records")

    # ── Operações ─────────────────────────────────────────────────────────
    def adicionar(self, aluno: Aluno) -> None:
        """Adiciona aluno. Lança ValueError se já existir."""
        df = self._carregar()
        if aluno.nome in df["Aluno"].values:
            raise ValueError(f"Aluno '{aluno.nome}' já cadastrado.")
        media, situacao = self.calcular_situacao(aluno.nota1, aluno.nota2)
        nova_linha = pd.DataFrame([{
            "Aluno": aluno.nome, "Nota1": aluno.nota1,
            "Nota2": aluno.nota2, "Média": media, "Situação": situacao
        }])
        df = pd.concat([df, nova_linha], ignore_index=True)
        self._salvar(df)

    def atualizar(self, nome_original: str, aluno: Aluno) -> None:
        """Atualiza os dados de um aluno existente."""
        df = self._carregar()
        media, situacao = self.calcular_situacao(aluno.nota1, aluno.nota2)
        mask = df["Aluno"] == nome_original
        df.loc[mask, ["Aluno", "Nota1", "Nota2", "Média", "Situação"]] = [
            aluno.nome, aluno.nota1, aluno.nota2, media, situacao
        ]
        self._salvar(df)

    def remover(self, nome: str) -> None:
        """Remove um aluno pelo nome."""
        df = self._carregar()
        df = df[df["Aluno"] != nome].reset_index(drop=True)
        self._salvar(df)
