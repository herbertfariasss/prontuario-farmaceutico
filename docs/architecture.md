# Arquitetura do Prontuário Farmacêutico

## Objetivo

Sistema web local para gerenciamento de prontuário eletrônico
farmacêutico, desenvolvido em Python e Streamlit.

## Camadas

### Presentation

Interface construída com Streamlit.

Responsável por:
- renderização das telas;
- entrada de dados;
- navegação;
- mensagens ao usuário.

### Application

Contém os casos de uso da aplicação.

Exemplos:
- autenticação;
- criação de paciente;
- atualização de paciente;
- criação de atendimento;
- geração de documentos;
- backup;
- auditoria.

### Domain

Contém as entidades e regras centrais do sistema.

Entidades principais:
- User
- Professional
- Patient
- Encounter
- Document

### Infrastructure

Responsável por:
- banco de dados;
- SQLCipher;
- autenticação;
- armazenamento de chaves;
- geração de PDF;
- logs;
- backup.

## Banco de dados

SQLite protegido com SQLCipher.

O banco será armazenado localmente.

## Segurança

Os dados do banco serão criptografados em repouso.

Senhas não serão armazenadas em texto puro.

Chaves criptográficas não serão armazenadas no código-fonte.

## Fluxo principal

Login
→ busca de paciente
→ abertura do paciente
→ novo atendimento
→ preenchimento SOAP
→ salvamento
→ geração de documento