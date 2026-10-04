# Segurança

## Banco de dados

O banco de dados utiliza SQLCipher para criptografia em repouso.

## Senhas

As senhas dos usuários não são armazenadas em texto.

O sistema utiliza Argon2id para armazenamento seguro das credenciais.

## Controle de tentativas

A tabela usuarios possui campos para controlar:

- tentativas de autenticação;
- bloqueio temporário.

## Chaves

A chave do banco não deve ser armazenada no código-fonte.

Durante o desenvolvimento, ela pode ser fornecida por variável de ambiente.

Em produção, a aplicação deverá utilizar armazenamento seguro de credenciais do sistema operacional.

## Logs

Logs de auditoria não devem armazenar:

- senhas;
- hashes de senha;
- chaves criptográficas;
- dados clínicos desnecessários.

## Dados sensíveis

Informações de pacientes e atendimentos devem ser tratadas como dados sensíveis.

O sistema deve minimizar a exposição desses dados.