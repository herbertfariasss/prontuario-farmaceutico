import getpass

from src.infrastructure.database.conexao import obter_conexao
from src.infrastructure.database.repositorios.usuario import (
    UsuarioRepositorio,
)
from src.infrastructure.security.senhas import gerar_hash_senha

TAMANHO_MINIMO_SENHA = 12


def principal() -> None:
    nome_usuario = input(
        "Digite o nome de usuário: "
    ).strip().lower()

    if not nome_usuario:
        print("O nome de usuário não pode ser vazio.")
        return

    senha = getpass.getpass(
        "Digite a senha: "
    )

    confirmacao = getpass.getpass(
        "Confirme a senha: "
    )

    if senha != confirmacao:
        print("As senhas não coincidem.")
        return

    if len(senha) < TAMANHO_MINIMO_SENHA:
        print(
            "A senha deve possuir pelo menos "
            f"{TAMANHO_MINIMO_SENHA} caracteres."
        )
        return

    hash_senha = gerar_hash_senha(senha)

    repositorio = UsuarioRepositorio()
    conexao = obter_conexao()

    try:
        usuario_existente = (
            repositorio.buscar_por_nome_usuario(
                nome_usuario,
                conexao=conexao,
            )
        )

        if usuario_existente:
            print("Esse usuário já existe.")
            return

        usuario_id = repositorio.criar(
            nome_usuario=nome_usuario,
            hash_senha=hash_senha,
            conexao=conexao,
        )

        print(
            f"Usuário criado com sucesso. ID: {usuario_id}"
        )

    finally:
        conexao.close()


if __name__ == "__main__":
    principal()