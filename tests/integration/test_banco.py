import pytest
import sqlcipher3.dbapi2 as sqlite3

from src.infrastructure.database.conexao import obter_conexao
from src.infrastructure.database.migrador import aplicar_migracoes


def test_esquema_do_banco_e_criado(tmp_path):
    caminho_banco = tmp_path / "teste.db"

    conexao = obter_conexao(
        caminho_banco=caminho_banco,
        chave="chave-de-teste",
    )

    try:
        aplicar_migracoes(conexao)

        tabelas = conexao.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        ).fetchall()

        nomes_tabelas = {
            tabela["name"]
            for tabela in tabelas
        }

        assert "usuarios" in nomes_tabelas
        assert "profissionais" in nomes_tabelas
        assert "pacientes" in nomes_tabelas
        assert "atendimentos" in nomes_tabelas
        assert "documentos" in nomes_tabelas
        assert "logs_auditoria" in nomes_tabelas
        assert "migracoes" in nomes_tabelas

    finally:
        conexao.close()


def test_chaves_estrangeiras_estao_ativadas(tmp_path):
    caminho_banco = tmp_path / "teste.db"

    conexao = obter_conexao(
        caminho_banco=caminho_banco,
        chave="chave-de-teste",
    )

    try:
        aplicar_migracoes(conexao)

        resultado = conexao.execute(
            "PRAGMA foreign_keys"
        ).fetchone()

        assert resultado[0] == 1

    finally:
        conexao.close()


def test_chave_estrangeira_invalida_e_rejeitada(tmp_path):
    caminho_banco = tmp_path / "teste.db"

    conexao = obter_conexao(
        caminho_banco=caminho_banco,
        chave="chave-de-teste",
    )

    try:
        aplicar_migracoes(conexao)

        with pytest.raises(sqlite3.IntegrityError):
            conexao.execute(
                """
                INSERT INTO atendimentos (
                    paciente_id,
                    profissional_id,
                    subjetivo,
                    objetivo,
                    avaliacao,
                    plano
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    999,
                    999,
                    "Teste",
                    "Teste",
                    "Teste",
                    "Teste",
                ),
            )

    finally:
        conexao.close()