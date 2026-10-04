from pathlib import Path

import sqlcipher3.dbapi2 as sqlite3

DATABASE_PATH = Path("data/test_encrypted.db")
DATABASE_KEY = "development-test-key"


def main() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        # PRAGMA não aceita placeholders (?).
        # Escapamos aspas simples para evitar quebrar a instrução SQL.
        escaped_key = DATABASE_KEY.replace("'", "''")
        cursor.execute(f"PRAGMA key = '{escaped_key}'")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS test_data (
                id INTEGER PRIMARY KEY,
                message TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            INSERT INTO test_data (message)
            VALUES (?)
            """,
            ("SQLCipher funcionando",),
        )

        connection.commit()

        cursor.execute(
            """
            SELECT message
            FROM test_data
            ORDER BY id DESC
            LIMIT 1
            """
        )

        result = cursor.fetchone()

        if result:
            print(result[0])
        else:
            print("Nenhum resultado encontrado.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()