from src.application.servico_autenticacao import (
    MAXIMO_TENTATIVAS,
    ServicoAutenticacao,
)
from src.infrastructure.database.conexao import obter_conexao
from src.infrastructure.database.repositorios.usuario import (
    UsuarioRepositorio,
)
from src.infrastructure.security.senhas import gerar_hash_senha


def criar_usuario_teste(conexao):
    repositorio = UsuarioRepositorio()

    return repositorio.criar(
        nome_usuario="teste",
        hash_senha=gerar_hash_senha(
            "SenhaSegura123!"
        ),
        conexao=conexao,
    )


def test_login_com_senha_correta(tmp_path):
    caminho_banco = tmp_path / "teste.db"

    conexao = obter_conexao(
        caminho_banco=caminho_banco,
        chave="chave-teste",
    )

    try:
        from src.infrastructure.database.migrador import (
            aplicar_migracoes,
        )

        aplicar_migracoes(conexao)
        criar_usuario_teste(conexao)

        servico = ServicoAutenticacao()

        resultado = servico.autenticar(
            "teste",
            "SenhaSegura123!",
            conexao=conexao,
        )

        assert resultado.sucesso is True
        assert resultado.usuario_id == 1

    finally:
        conexao.close()


def test_login_com_senha_incorreta(tmp_path):
    caminho_banco = tmp_path / "teste.db"

    conexao = obter_conexao(
        caminho_banco=caminho_banco,
        chave="chave-teste",
    )

    try:
        from src.infrastructure.database.migrador import (
            aplicar_migracoes,
        )

        aplicar_migracoes(conexao)
        criar_usuario_teste(conexao)

        servico = ServicoAutenticacao()

        resultado = servico.autenticar(
            "teste",
            "senha-errada",
            conexao=conexao,
        )

        assert resultado.sucesso is False
        assert resultado.mensagem == (
            "Usuário ou senha inválidos."
        )

    finally:
        conexao.close()


def test_usuario_e_bloqueado_apos_cinco_falhas(tmp_path):
    caminho_banco = tmp_path / "teste.db"

    conexao = obter_conexao(
        caminho_banco=caminho_banco,
        chave="chave-teste",
    )

    try:
        from src.infrastructure.database.migrador import (
            aplicar_migracoes,
        )

        aplicar_migracoes(conexao)

        usuario_id = criar_usuario_teste(conexao)

        servico = ServicoAutenticacao()

        for _ in range(MAXIMO_TENTATIVAS):
            servico.autenticar(
                "teste",
                "senha-errada",
                conexao=conexao,
            )

        usuario = conexao.execute(
            """
            SELECT
                tentativas_falhas,
                bloqueado_ate
            FROM usuarios
            WHERE id = ?
            """,
            (usuario_id,),
        ).fetchone()

        assert usuario["tentativas_falhas"] == MAXIMO_TENTATIVAS
        assert usuario["bloqueado_ate"] is not None

    finally:
        conexao.close()


def test_login_nao_funciona_enquanto_usuario_estiver_bloqueado(
    tmp_path,
):
    caminho_banco = tmp_path / "teste.db"

    conexao = obter_conexao(
        caminho_banco=caminho_banco,
        chave="chave-teste",
    )

    try:
        from src.infrastructure.database.migrador import (
            aplicar_migracoes,
        )

        aplicar_migracoes(conexao)
        criar_usuario_teste(conexao)

        servico = ServicoAutenticacao()

        for _ in range(MAXIMO_TENTATIVAS):
            servico.autenticar(
                "teste",
                "senha-errada",
                conexao=conexao,
            )

        resultado = servico.autenticar(
            "teste",
            "SenhaSegura123!",
            conexao=conexao,
        )

        assert resultado.sucesso is False

    finally:
        conexao.close()


def test_login_bem_sucedido_reseta_tentativas(tmp_path):
    caminho_banco = tmp_path / "teste.db"

    conexao = obter_conexao(
        caminho_banco=caminho_banco,
        chave="chave-teste",
    )

    try:
        from src.infrastructure.database.migrador import (
            aplicar_migracoes,
        )

        aplicar_migracoes(conexao)
        criar_usuario_teste(conexao)

        servico = ServicoAutenticacao()

        servico.autenticar(
            "teste",
            "senha-errada",
            conexao=conexao,
        )

        resultado = servico.autenticar(
            "teste",
            "SenhaSegura123!",
            conexao=conexao,
        )

        assert resultado.sucesso is True

        usuario = conexao.execute(
            """
            SELECT
                tentativas_falhas,
                bloqueado_ate,
                ultimo_login_em
            FROM usuarios
            WHERE id = 1
            """
        ).fetchone()

        assert usuario["tentativas_falhas"] == 0
        assert usuario["bloqueado_ate"] is None
        assert usuario["ultimo_login_em"] is not None

    finally:
        conexao.close()