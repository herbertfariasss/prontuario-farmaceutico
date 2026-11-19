# Prontuário Farmacêutico

Protótipo de um prontuário eletrônico para atendimento farmacêutico. O projeto usa Python, Streamlit e SQLCipher para desenvolver uma aplicação local.

## Estado atual

A interface Streamlit exibe a tela inicial. O repositório já inclui migrações do banco, autenticação com hash de senha Argon2id, auditoria de login e testes. O fluxo de atendimento e a geração de documentos estão previstos na arquitetura. Use dados fictícios durante o desenvolvimento.

## Como executar no Windows

No PowerShell, dentro do repositório, crie um ambiente virtual, instale as dependências e inicie a interface:

```powershell
git clone https://github.com/herbertfariasss/prontuario-farmaceutico.git
cd prontuario-farmaceutico
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### Banco local e testes

Para inicializar o banco de desenvolvimento, defina a variável de ambiente `PRONTUARIO_DB_KEY` na sessão do terminal com uma chave própria e mantenha esse valor fora do Git. Use a mesma chave nas sessões em que precisar abrir o banco local já criado.

```powershell
.\.venv\Scripts\python.exe -m scripts.inicializar_banco
.\.venv\Scripts\python.exe -m scripts.criar_usuario
.\.venv\Scripts\python.exe -m pytest
```

O comando de criação de usuário é interativo. Os testes usam bancos temporários e chaves de teste.

## Documentação

- [Arquitetura e fluxo planejado](docs/architecture.md)
- [Modelo de dados](docs/database.md)
- [Segurança e armazenamento de chaves](docs/seguranca.md)
