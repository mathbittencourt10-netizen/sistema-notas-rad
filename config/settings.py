# Credenciais de acesso ao sistema
USUARIOS = {
    "professor": {"senha": "prof123", "tipo": "professor", "nome": "Professor"},
    "ana":       {"senha": "1234",    "tipo": "aluno",     "nome": "Ana Silva"},
    "joao":      {"senha": "1234",    "tipo": "aluno",     "nome": "João Oliveira"},
    "maria":     {"senha": "1234",    "tipo": "aluno",     "nome": "Maria Santos"},
}

# Arquivo de dados
ARQUIVO_DADOS = "notas_alunos.xlsx"

# Colunas da planilha
COLUNAS = ["Aluno", "Nota1", "Nota2", "Média", "Situação"]

# Critérios de avaliação
NOTA_APROVACAO   = 7.0
NOTA_RECUPERACAO = 5.0
