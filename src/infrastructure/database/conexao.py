import os
from pathlib import Path

import sqlcipher3.dbapi2 as sqlite3

CAMINHO_BANCO_PADRAO = Path("data/prontuario.db")
VARIAVEL_CHAVE_BANCO = "PRONTUARIO_DB_KEY"


def obter_chave_banco() -> str:
    chave = os.getenv(VARIAVEL_CHAVE_BANCO)

    if not chave:
        raise RuntimeError(
            f"A variável de ambiente {VARIAVEL_CHAVE_BANCO} "
            "não foi configurada."
        )

    return chave


def escapar_valor_pragma(valor: str) -> str:
    return valor.replace("'", "''")


def obter_conexao(
    caminho_banco: Path | str = CAMINHO_BANCO_PADRAO,
    chave: str | None = None,
):
    caminho_banco = Path(caminho_banco)
    caminho_banco.parent.mkdir(parents=True, exist_ok=True)

    chave_banco = chave or obter_chave_banco()
    chave_escapada = escapar_valor_pragma(chave_banco)

    conexao = sqlite3.connect(caminho_banco)

    try:
        conexao.execute(f"PRAGMA key = '{chave_escapada}'")
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.execute("PRAGMA busy_timeout = 5000")

        conexao.row_factory = sqlite3.Row

        return conexao

    except Exception:
        conexao.close()
        raise