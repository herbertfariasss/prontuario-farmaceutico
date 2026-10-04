from pathlib import Path

from .conexao import obter_conexao

PASTA_MIGRACOES = Path(__file__).parent / "migrations"


def criar_tabela_migracoes(conexao) -> None:
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS migracoes (
            versao TEXT PRIMARY KEY,
            aplicada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conexao.commit()


def obter_migracoes_aplicadas(conexao) -> set[str]:
    linhas = conexao.execute(
        """
        SELECT versao
        FROM migracoes
        """
    ).fetchall()

    return {linha["versao"] for linha in linhas}


def aplicar_migracoes(conexao=None) -> list[str]:
    propria_conexao = conexao is None

    if propria_conexao:
        conexao = obter_conexao()

    try:
        criar_tabela_migracoes(conexao)

        migracoes_aplicadas = obter_migracoes_aplicadas(conexao)
        versoes_aplicadas: list[str] = []

        arquivos_migracao = sorted(
            PASTA_MIGRACOES.glob("*.sql")
        )

        for arquivo_migracao in arquivos_migracao:
            versao = arquivo_migracao.stem.split(
                "_",
                maxsplit=1,
            )[0]

            if versao in migracoes_aplicadas:
                continue

            sql = arquivo_migracao.read_text(
                encoding="utf-8"
            )

            conexao.executescript(sql)

            conexao.execute(
                """
                INSERT INTO migracoes (versao)
                VALUES (?)
                """,
                (versao,),
            )

            conexao.commit()

            versoes_aplicadas.append(versao)

        return versoes_aplicadas

    finally:
        if propria_conexao:
            conexao.close()