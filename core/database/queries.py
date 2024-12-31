from core.settings import settings

import asyncpg


async def execute_query(query, values=None):
    conn = await asyncpg.connect(settings.bots.db_link)
    try:
        if values:
            await conn.execute(query, *values)
        else:
            await conn.execute(query)
    except Exception as e:
        print(f"ОШибка: {e}")
        raise Exception
    finally:
        await conn.close()


async def create_short_id(short_id, file_id, content_type):
    query = """
        INSERT INTO
            short_id (id, file_id, content_type) VALUES ($1, $2, $3)
    """

    values = (short_id, file_id, content_type)
    return await execute_query(query, values)


async def create_user(message):
    query = f"""
        INSERT INTO
            users (telegram_id, user_name, user_alias)
        VALUES ($1, $2, $3)
    """
    values = (message.from_user.id, message.from_user.full_name, message.from_user.username)
    return await execute_query(query, values)


async def set_ban(telegram_id, time_to_unban):
    query = """
        UPDATE
            users
        SET
            ban_status = 1,
            time_to_unban = $1
        WHERE
            telegram_id = $2
        """
    values = (time_to_unban, telegram_id,)
    return await execute_query(query, values)


async def set_unban(telegram_id):
    query = """
            UPDATE
                users
            SET
                ban_status = 0
            WHERE
                telegram_id = $1
            """
    values = (telegram_id,)
    return await execute_query(query, values)


async def get_time_to_unban(telegram_id):
    query = """
        SELECT time_to_unban
        FROM users
        WHERE telegram_id = $1
        """
    values = (telegram_id,)
    return await execute_read_query(query, values)


async def increase_message_counter(telegram_id):
    query = """
    UPDATE
        users
    SET
        message_counter = message_counter + 1
    WHERE
        telegram_id = $1
    """
    values = (telegram_id,)
    return await execute_query(query, values)


async def increase_approved_message_counter(telegram_id):
    query = f"""
    UPDATE
        users
    SET
        approved_memes_counter = approved_memes_counter + 1
    WHERE
        telegram_id = {telegram_id}
    """

    return await execute_query(query)


async def increase_rejected_message_counter(telegram_id):
    query = f"""
        UPDATE
            users
        SET
            rejected_message_counter = rejected_message_counter + 1
        WHERE
            telegram_id = {telegram_id}
        """

    return await execute_query(query)


async def add_post_to_scheduler(post_id, send_time, content_type, author):
    query = ("INSERT INTO "
             "scheduler (file_id, send_time, content_type, author) "
             "VALUES ($1, $2, $3, $4)")
    values = (post_id, send_time, content_type, author,)
    return await execute_query(query, values)


async def delete_sent_post(id):
    query = "DELETE FROM scheduler WHERE id = $1"
    values = (id,)
    return await execute_query(query, values)


async def execute_read_query(query, values=None):
    conn = await asyncpg.connect(settings.bots.db_link)
    result = None
    try:
        if values:
            result = await conn.fetch(query, *values)
            print("запрос в базу", result)
        else:
            result = await conn.fetch(query)
        return result
    except Exception as e:
        print(f"ОШЫБКА{e}")
        raise Exception
    finally:
        await conn.close()


async def check_user(telegram_id):
    query = "SELECT EXISTS(SELECT * FROM users WHERE telegram_id = $1)"
    valuse = (telegram_id,)
    return await execute_read_query(query, valuse)


async def get_ban_status(telegram_id):
    query = 'SELECT ban_status FROM users WHERE telegram_id = $1'
    values = (telegram_id,)
    return await execute_read_query(query, values)


async def get_statistic(telegram_id):
    query = '''
            SELECT
            user_name, user_alias, message_counter, approved_memes_counter, rejected_message_counter
            FROM users
            WHERE telegram_id = $1
        '''
    values = (telegram_id,)
    return await execute_read_query(query, values)


async def get_ban_users():
    query = "SELECT * FROM users WHERE ban_status = 1"
    return await execute_read_query(query)


async def get_file_id(short_id):
    query = "SELECT file_id FROM short_id where id = $1"
    values = (short_id,)
    result = execute_read_query(query, values)
    return await result


async def check_schedule_post():
    query = 'SELECT EXISTS(SELECT * FROM scheduler)'
    return await execute_read_query(query)


async def get_time_last_post():
    query = "SELECT MAX(send_time) FROM scheduler"
    return await execute_read_query(query)


async def get_posts(time):
    query = "SELECT id, file_id, content_type, author FROM scheduler WHERE send_time <= $1"
    values = (time,)
    return await execute_read_query(query, values)


async def get_content_type(short_id):
    query = "SELECT content_type FROM short_id where id = $1"
    values = (short_id,)
    result = execute_read_query(query, values)
    return await result


async def get_posts_quantity():
    query = 'SELECT COUNT(*) FROM scheduler'
    return await execute_read_query(query)
