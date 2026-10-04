# Modelo de Dados

## users

Responsável pela autenticação.

Campos:

- id
- username
- password_hash
- is_active
- created_at
- last_login_at

---

## professionals

Dados do profissional responsável pelo atendimento.

Campos:

- id
- user_id
- full_name
- crf
- address
- phone
- created_at
- updated_at

---

## patients

Dados cadastrais do paciente.

Campos:

- id
- full_name
- cpf
- birth_date
- phone
- observations
- allergies
- created_at
- updated_at
- is_active

---

## encounters

Representa um atendimento farmacêutico.

Campos:

- id
- patient_id
- professional_id
- occurred_at
- subjective
- objective
- assessment
- plan
- created_at
- updated_at

---

## documents

Representa documentos gerados a partir de um atendimento.

Tipos previstos:

- prescription
- exam_request
- referral

Campos:

- id
- encounter_id
- document_type
- created_at
- metadata

---

## audit_logs

Registra ações relevantes realizadas no sistema.

Exemplos:

- LOGIN_SUCCESS
- LOGIN_FAILED
- PATIENT_CREATED
- PATIENT_UPDATED
- ENCOUNTER_CREATED
- DOCUMENT_GENERATED
- BACKUP_CREATED

Os logs não devem armazenar conteúdo clínico desnecessário.