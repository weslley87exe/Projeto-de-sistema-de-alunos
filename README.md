# API Sistema de Alunos

Essa API gerencia um sistema simples de cadastro de alunos.

## Estrutura
- **models.py**: Define as tabelas do banco
- **schemas.py**: Validação de dados (Pydantic)
- **crud.py**: Funções de Create, Read, Update, Delete
- **database.py**: Conexão com o banco
- **main.py**: Entrada da API, define rotas
- **config.py**: Configurações do projeto
- **.env.example**: Variáveis de ambiente

## Instalação

1. Criar ambiente virtual:
```bash
python -m venv venv
