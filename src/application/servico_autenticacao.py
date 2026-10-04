from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from src.infrastructure.database.conexao import obter_conexao
from src.infrastructure.database.repositorios.log_auditoria import (
    LogAuditoriaRepositorio,
)
from src.infrastructure.database.repositorios.usuario import (
    UsuarioRepositorio,
)
from src.infrastructure.security.senhas import verificar_senha

MAXIMO_TENTATIVAS = 5
MINUTOS_BLOQUEIO = 15


@dataclass(frozen=True)
class ResultadoAutenticacao:
    sucesso: bool
    usuario_id: int | None = None
    nome_usuario: str | None = None
    mensagem: str = ""


class ServicoAutenticacao:
    def __init__(
        self,
        usuario_repositorio: UsuarioRepositorio | None = None,
        log_repositorio: LogAuditoriaRepositorio | None = None,
    ):
        self.usuario_repositorio = (
            usuario_repositorio or UsuarioRepositorio()
        )

        self.log_repositorio = (
            log_repositorio or LogAuditoriaRepositorio()
        )

    @staticmethod
    def _agora() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def _converter_data(
        data: str | None,
    ) -> datetime | None:
        if not data:
            return None

        return datetime.fromisoformat(data)

    def autenticar(
        self,
        nome_usuario: str,
        senha: str,
        conexao=None,
    ) -> ResultadoAutenticacao:
        nome_usuario = nome_usuario.strip().lower()

        if not nome_usuario or not senha:
            return ResultadoAutenticacao(
                sucesso=False,
                mensagem="Usuário ou senha inválidos.",
            )

        propria_conexao = conexao is None

        if propria_conexao:
            conexao = obter_conexao()

        try:
            usuario = self.usuario_repositorio.buscar_por_nome_usuario(
                nome_usuario,
                conexao=conexao,
            )

            if usuario is None:
                return ResultadoAutenticacao(
                    sucesso=False,
                    mensagem="Usuário ou senha inválidos.",
                )

            if not usuario["ativo"]:
                self.log_repositorio.registrar(
                    conexao=conexao,
                    acao="LOGIN_FALHA",
                    usuario_id=usuario["id"],
                    entidade="usuarios",
                    entidade_id=usuario["id"],
                    metadados={
                        "motivo": "usuario_inativo",
                    },
                )

                conexao.commit()

                return ResultadoAutenticacao(
                    sucesso=False,
                    mensagem="Usuário ou senha inválidos.",
                )

            agora = self._agora()

            bloqueado_ate = self._converter_data(
                usuario["bloqueado_ate"]
            )

            if bloqueado_ate and agora < bloqueado_ate:
                self.log_repositorio.registrar(
                    conexao=conexao,
                    acao="LOGIN_FALHA",
                    usuario_id=usuario["id"],
                    entidade="usuarios",
                    entidade_id=usuario["id"],
                    metadados={
                        "motivo": "usuario_bloqueado",
                    },
                )

                conexao.commit()

                return ResultadoAutenticacao(
                    sucesso=False,
                    mensagem="Usuário ou senha inválidos.",
                )

            if bloqueado_ate and agora >= bloqueado_ate:
                conexao.execute(
                    """
                    UPDATE usuarios
                    SET
                        tentativas_falhas = 0,
                        bloqueado_ate = NULL
                    WHERE id = ?
                    """,
                    (usuario["id"],),
                )

                conexao.commit()

                usuario = (
                    self.usuario_repositorio
                    .buscar_por_nome_usuario(
                        nome_usuario,
                        conexao=conexao,
                    )
                )

            senha_valida = verificar_senha(
                senha,
                usuario["hash_senha"],
            )

            if senha_valida:
                self.usuario_repositorio.registrar_login_sucesso(
                    usuario["id"],
                    conexao=conexao,
                )

                self.log_repositorio.registrar(
                    conexao=conexao,
                    acao="LOGIN_SUCESSO",
                    usuario_id=usuario["id"],
                    entidade="usuarios",
                    entidade_id=usuario["id"],
                )

                conexao.commit()

                return ResultadoAutenticacao(
                    sucesso=True,
                    usuario_id=usuario["id"],
                    nome_usuario=usuario["nome_usuario"],
                    mensagem="Login realizado com sucesso.",
                )

            novas_tentativas = usuario["tentativas_falhas"] + 1
            novo_bloqueio = None

            if novas_tentativas >= MAXIMO_TENTATIVAS:
                novo_bloqueio = (
                    agora
                    + timedelta(minutes=MINUTOS_BLOQUEIO)
                ).isoformat()

            self.usuario_repositorio.registrar_login_falho(
                usuario_id=usuario["id"],
                tentativas_falhas=novas_tentativas,
                bloqueado_ate=novo_bloqueio,
                conexao=conexao,
            )

            self.log_repositorio.registrar(
                conexao=conexao,
                acao="LOGIN_FALHA",
                usuario_id=usuario["id"],
                entidade="usuarios",
                entidade_id=usuario["id"],
                metadados={
                    "motivo": "credencial_invalida",
                },
            )

            if novo_bloqueio:
                self.log_repositorio.registrar(
                    conexao=conexao,
                    acao="USUARIO_BLOQUEADO",
                    usuario_id=usuario["id"],
                    entidade="usuarios",
                    entidade_id=usuario["id"],
                    metadados={
                        "duracao_minutos": MINUTOS_BLOQUEIO,
                    },
                )

            conexao.commit()

            return ResultadoAutenticacao(
                sucesso=False,
                mensagem="Usuário ou senha inválidos.",
            )

        finally:
            if propria_conexao:
                conexao.close()