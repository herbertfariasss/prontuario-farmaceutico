from src.infrastructure.database.conexao import obter_conexao
from src.infrastructure.database.migrador import aplicar_migracoes


def principal() -> None:
    conexao = obter_conexao()

    try:
        aplicadas = aplicar_migracoes(conexao)

        if aplicadas:
            print(
                f"Migrações aplicadas: {', '.join(aplicadas)}"
            )
        else:
            print("Banco de dados já está atualizado.")

    finally:
        conexao.close()


if __name__ == "__main__":
    principal()