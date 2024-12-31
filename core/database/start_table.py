import asyncpg

from core.settings import settings


def create_table_short_id():
    query = """
    CREATE TABLE IF NOT EXISTS short_id (
        id TEXT PRIMARY KEY,
        file_id TEXT,
        content_type TEXT
    )
    """
    return query


def create_table_scheduler():
    query = """
        CREATE TABLE IF NOT EXISTS scheduler (
        id SERIAL PRIMARY KEY,
        file_id TEXT NOT NULL,
        send_time TIMESTAMP NOT NULL,
        content_type TEXT NOT NULL,
        author TEXT NOT NULL
        )
    """
    return query


def create_user_table():
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT,
        user_name TEXT,
        user_alias TEXT,
        message_counter INTEGER DEFAULT 0,
        approved_memes_counter INTEGER DEFAULT 0,
        rejected_message_counter INTEGER DEFAULT 0,
        ban_status INTEGER DEFAULT 0,
        time_to_unban TIMESTAMP
    )
    """
    return query


async def create_all_tables():
    conn = await asyncpg.connect(settings.bots.db_link)
    query_user_table = create_user_table()
    query_short_id_table = create_table_short_id()
    query_scheduler_table = create_table_scheduler()
    await conn.execute(query_user_table)
    await conn.execute(query_short_id_table)
    await conn.execute(query_scheduler_table)
    await conn.close()
