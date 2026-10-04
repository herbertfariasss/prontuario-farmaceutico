from src.infrastructure.security.senhas import (
    gerar_hash_senha,
    precisa_rehash,
    verificar_senha,
)


def test_deve_gerar_hash_de_senha():
    senha = "SenhaDeTeste!2026"

    hash_senha = gerar_hash_senha(senha)

    assert hash_senha != senha
    assert hash_senha.startswith("$argon2id$")


def test_deve_verificar_senha_correta():
    senha = "SenhaDeTeste!2026"

    hash_senha = gerar_hash_senha(senha)

    assert verificar_senha(senha, hash_senha) is True


def test_deve_rejeitar_senha_incorreta():
    senha = "SenhaDeTeste!2026"

    hash_senha = gerar_hash_senha(senha)

    assert verificar_senha("SenhaErrada", hash_senha) is False


def test_hashes_da_mesma_senha_devem_ser_diferentes():
    senha = "SenhaDeTeste!2026"

    primeiro_hash = gerar_hash_senha(senha)
    segundo_hash = gerar_hash_senha(senha)

    assert primeiro_hash != segundo_hash

    assert verificar_senha(senha, primeiro_hash) is True
    assert verificar_senha(senha, segundo_hash) is True


def test_hash_atual_nao_deve_precisar_de_rehash():
    senha = "SenhaDeTeste!2026"

    hash_senha = gerar_hash_senha(senha)

    assert precisa_rehash(hash_senha) is False