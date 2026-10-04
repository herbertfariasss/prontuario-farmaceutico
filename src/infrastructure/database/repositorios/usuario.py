from datetime import datetime, timezone

from src.infrastructure.database.conexao import obter_conexao


class UsuarioRepositorio:
    def buscar_por_nome_usuario(
        self,
        nome_usuario: str,
        conexao=None,
    ):
        propria_conexao = conexao is None

        if propria_conexao:
            conexao = obter_conexao()

        try:
            return conexao.execute(
                """
                SELECT
                    id,
                    nome_usuario,
                    hash_senha,
                    ativo,
                    criado_em,
                    ultimo_login_em,
                    tentativas_falhas,
                    bloqueado_ate
                FROM usuarios
                WHERE nome_usuario = ?
                """,
                (nome_usuario,),
            ).fetchone()

        finally:
            if propria_conexao:
                conexao.close()

    def criar(
        self,
        nome_usuario: str,
        hash_senha: str,
        conexao=None,
    ) -> int:
        propria_conexao = conexao is None

        if propria_conexao:
            conexao = obter_conexao()

        try:
            cursor = conexao.execute(
                """
                INSERT INTO usuarios (
                    nome_usuario,
                    hash_senha
                )
                VALUES (?, ?)
                """,
                (
                    nome_usuario,
                    hash_senha,
                ),
            )

            conexao.commit()

            return cursor.lastrowid

        finally:
            if propria_conexao:
                conexao.close()

    def registrar_login_sucesso(
        self,
        usuario_id: int,
        conexao=None,
    ) -> None:
        propria_conexao = conexao is None

        if propria_conexao:
            conexao = obter_conexao()

        try:
            agora = datetime.now(timezone.utc).isoformat()

            conexao.execute(
                """
                UPDATE usuarios
                SET
                    tentativas_falhas = 0,
                    bloqueado_ate = NULL,
                    ultimo_login_em = ?
                WHERE id = ?
                """,
                (
                    agora,
                    usuario_id,
                ),
            )

            conexao.commit()

        finally:
            if propria_conexao:
                conexao.close()

    def registrar_login_falho(
        self,
        usuario_id: int,
        tentativas_falhas: int,
        bloqueado_ate: str | None,
        conexao=None,
    ) -> None:
        propria_conexao = conexao is None

        if propria_conexao:
            conexao = obter_conexao()

        try:
            conexao.execute(
                """
                UPDATE usuarios
                SET
                    tentativas_falhas = ?,
                    bloqueado_ate = ?
                WHERE id = ?
                """,
                (
                    tentativas_falhas,
                    bloqueado_ate,
                    usuario_id,
                ),
            )

            conexao.commit()

        finally:
            if propria_conexao:
                conexao.close()