import pytest

from database import PgConnection



@pytest.mark.asyncio
async def test_successful_connection():
    """Test successful database connection with real PostgreSQL."""
    conn = PgConnection()

    async with conn as pg:
        assert pg._connection_ is not None
        assert pg.cursor is not None

        await pg.cursor.execute("SELECT 1")
        result = await pg.cursor.fetchone()
        assert result[0] == 1