from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

HASH_SENHA = PasswordHasher(
    time_cost=2,
    memory_cost=19_456,
    parallelism=1,
    hash_len=32,
    salt_len=16,
)


def gerar_hash_senha(senha: str) -> str:
    if not senha:
        raise ValueError("A senha não pode ser vazia.")

    return HASH_SENHA.hash(senha)


def verificar_senha(senha: str, hash_senha: str) -> bool:
    if not senha or not hash_senha:
        return False

    try:
        return HASH_SENHA.verify(hash_senha, senha)
    except (VerifyMismatchError, InvalidHashError):
        return False


def precisa_rehash(hash_senha: str) -> bool:
    return HASH_SENHA.check_needs_rehash(hash_senha)