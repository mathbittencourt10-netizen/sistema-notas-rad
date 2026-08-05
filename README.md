# 📚 Sistema de Notas — RAD com Python

Sistema desktop de controle de notas com autenticação por perfil (professor/aluno),  
desenvolvido com Python, tkinter e pandas. Dados persistidos em Excel (.xlsx).

---

## 🚀 Funcionalidades

### 👨‍🏫 Professor
- Cadastrar alunos com duas notas
- Cálculo automático de média e situação
- Editar e excluir registros
- Busca em tempo real por nome
- Cores por situação na tabela

### 👨‍🎓 Aluno
- Visualizar apenas as próprias notas
- Interface simplificada (somente leitura)

---

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-FF6F00?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)

---

## 📁 Estrutura do projeto

```
sistema-notas-rad/
├── main.py                          # Ponto de entrada
├── requirements.txt
├── config/
│   └── settings.py                  # Credenciais e configurações
├── models/
│   ├── usuario.py                   # Modelo de usuário
│   └── aluno.py                     # Modelo de aluno/nota
├── controllers/
│   ├── auth_controller.py           # Autenticação
│   └── nota_controller.py           # CRUD com pandas/Excel
└── views/
    ├── login_view.py                # Tela de login
    ├── professor_view.py            # Dashboard do professor
    └── aluno_view.py                # Visualização do aluno
```

---

## ⚙️ Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/mathbittencourt10-netizen/sistema-notas-rad.git
cd sistema-notas-rad
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute
```bash
python main.py
```

---

## 👥 Credenciais de acesso

| Usuário | Senha | Perfil |
|---|---|---|
| `professor` | `prof123` | Acesso total |
| `ana` | `1234` | Aluno |
| `joao` | `1234` | Aluno |
| `maria` | `1234` | Aluno |

> Para adicionar usuários, edite `config/settings.py`.

---

## 📊 Critérios de avaliação

| Média | Situação |
|---|---|
| ≥ 7,0 | ✅ Aprovado |
| ≥ 5,0 | ⚠️ Em Recuperação |
| < 5,0 | ❌ Reprovado |

---

## 👨‍💻 Autor

**Matheus Bittencourt**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/matheus-bittencourt-3b31a3177)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mathbittencourt10-netizen)
