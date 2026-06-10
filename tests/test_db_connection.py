from sqlalchemy import text

from signalnoise.database.connection import (
    engine
)


def test_postgres_connection():

    with engine.connect() as conn:

        result = conn.execute(
            text("SELECT 1")
        )

        value = result.scalar()

        print()

        print(
            f"Connection Result: {value}"
        )

        assert value == 1