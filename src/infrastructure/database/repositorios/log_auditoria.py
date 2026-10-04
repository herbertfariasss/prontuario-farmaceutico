import json


class LogAuditoriaRepositorio:
    def registrar(
        self,
        conexao,
        acao: str,
        usuario_id: int | None = None,
        entidade: str | None = None,
        entidade_id: int | None = None,
        metadados: dict | None = None,
    ) -> None:
        metadados_json = (
            json.dumps(
                metadados,
                ensure_ascii=False,
            )
            if metadados
            else None
        )

        conexao.execute(
            """
            INSERT INTO logs_auditoria (
                usuario_id,
                acao,
                entidade,
                entidade_id,
                metadados_json
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                usuario_id,
                acao,
                entidade,
                entidade_id,
                metadados_json,
            ),
        )