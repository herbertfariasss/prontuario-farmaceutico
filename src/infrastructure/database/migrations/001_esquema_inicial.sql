CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT NOT NULL UNIQUE,
    hash_senha TEXT NOT NULL,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultimo_login_em TEXT
);

CREATE TABLE IF NOT EXISTS profissionais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL UNIQUE,
    nome_completo TEXT NOT NULL,
    crf TEXT NOT NULL,
    endereco TEXT NOT NULL,
    telefone TEXT,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_profissional_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    data_nascimento TEXT NOT NULL,
    telefone TEXT,
    observacoes TEXT,
    alergias TEXT,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);

CREATE TABLE IF NOT EXISTS atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    profissional_id INTEGER NOT NULL,
    realizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subjetivo TEXT NOT NULL,
    objetivo TEXT NOT NULL,
    avaliacao TEXT NOT NULL,
    plano TEXT NOT NULL,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_atendimento_paciente
        FOREIGN KEY (paciente_id)
        REFERENCES pacientes(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_atendimento_profissional
        FOREIGN KEY (profissional_id)
        REFERENCES profissionais(id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS documentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    atendimento_id INTEGER NOT NULL,
    tipo_documento TEXT NOT NULL CHECK (
        tipo_documento IN (
            'prescricao',
            'solicitacao_exames',
            'encaminhamento'
        )
    ),
    metadados_json TEXT,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_documento_atendimento
        FOREIGN KEY (atendimento_id)
        REFERENCES atendimentos(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logs_auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    acao TEXT NOT NULL,
    entidade TEXT,
    entidade_id INTEGER,
    metadados_json TEXT,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_log_auditoria_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_pacientes_nome
    ON pacientes(nome_completo COLLATE NOCASE);

CREATE INDEX IF NOT EXISTS idx_atendimentos_paciente_data
    ON atendimentos(paciente_id, realizado_em DESC);

CREATE INDEX IF NOT EXISTS idx_atendimentos_profissional_data
    ON atendimentos(profissional_id, realizado_em DESC);

CREATE INDEX IF NOT EXISTS idx_documentos_atendimento
    ON documentos(atendimento_id);

CREATE INDEX IF NOT EXISTS idx_logs_auditoria_usuario_data
    ON logs_auditoria(usuario_id, criado_em DESC);

CREATE INDEX IF NOT EXISTS idx_logs_auditoria_entidade
    ON logs_auditoria(entidade, entidade_id);