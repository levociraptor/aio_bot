import sqlite3
from sqlite3 import Error


def execute_query(query, values = None, bot = 'bot_db.db'):
    connection = sqlite3.connect(bot)
    cursor = connection.cursor()


    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f'Error: {e} occurred\n'
              f'{values}\n'
              f'{query}')
    finally:
        connection.close()


def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        user_name TEXT,
        user_alias TEXT,
        message_counter INTEGER DEFAULT 0,
        aprroved_memes_counter INTEGER DEFAULT 0,
        rejected_message_counter INTEGER DEFAULT 0,
        ban_status INTEGER DEFAULT 0
    )
    """
    execute_query(query)


def create_table_short_id():
    query = """
    CREATE TABLE IF NOT EXISTS short_id (
        id TEXT PRIMARY KEY, 
        file_id TEXT,
        content_type TEXT
    )
    """

    execute_query(query, bot = "short_id.db")


def create_table_sheduler():
    query = """
        CREATE TABLE IF NOT EXISTS sheduler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id TEXT NOT NULL,
        send_time TIMESTAMP NOT NULL,
        content_type TEXT NOT NULL
        )
    """

    execute_query(query, bot = "sheduler.db")

def create_short_id(short_id, file_id, content_type):
    query = """
        INSERT INTO 
            short_id (id, file_id, content_type) VALUES (?, ?, ?)
    """

    values = (short_id, file_id, content_type)
    execute_query(query, values, bot = "short_id.db")

def create_user(message):
    query = f"""
        INSERT INTO
            users (telegram_id, user_name, user_alias)
        VALUES (?, ?, ?)
    """
    values = (message.from_user.id, message.from_user.full_name, message.from_user.username)
    execute_query(query, values)


def set_ban(telegram_id):
    query = f"""
        UPDATE
            users
        SET 
            ban_status = 1
        WHERE 
            telegram_id = {telegram_id}
        """
    execute_query(query)


def set_unban(telegram_id):
    query = f"""
            UPDATE
                users
            SET 
                ban_status = 0
            WHERE 
                telegram_id = {telegram_id}
            """
    execute_query(query)


def increase_message_counter(telegram_id):
    query = f"""
    UPDATE
        users
    SET 
        message_counter = message_counter + 1
    WHERE 
        telegram_id = {telegram_id}
    """
    execute_query(query)


def increase_approved_message_counter(telegram_id):
    query = f"""
    UPDATE 
        users
    SET
        aprroved_memes_counter = aprroved_memes_counter + 1
    WHERE 
        telegram_id = {telegram_id}
    """

    execute_query(query)


def increase_rejected_message_counter(telegram_id):
    query = f"""
        UPDATE 
            users
        SET
            rejected_message_counter = rejected_message_counter + 1
        WHERE 
            telegram_id = {telegram_id}
        """

    execute_query(query)


def add_post_to_sheduler(post_id, send_time, content_type):
    query = ("INSERT INTO "
             "sheduler (file_id, send_time, content_type) "
             "VALUES (?, ?, ?)")
    values = (post_id, send_time, content_type)
    execute_query(query, values, bot='sheduler.db')


def delete_sent_post(id):
    query = "DELETE FROM sheduler WHERE id = ?"
    values = (id,)
    execute_query(query, values, bot="sheduler.db")

def execute_read_query(query, values = None, bot = "bot_db.db"):
    connection = sqlite3.connect(bot)
    cursor = connection.cursor()
    result = None
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        return result
    except Error as e:
        print(f'The error {e} occurred')
    finally:
        connection.close()


def check_user(telegram_id):
    query = f'SELECT EXISTS(SELECT * FROM users WHERE telegram_id = {telegram_id})'
    return execute_read_query(query)


def get_ban_status(telegram_id):
    query = f'SELECT ban_status FROM users WHERE telegram_id = ?'
    values = (telegram_id,)
    result = execute_read_query(query, values)
    print(result)
    return result


def get_statistic(telegram_id):
    query = f'''SELECT
                user_name, user_alias, message_counter, aprroved_memes_counter, rejected_message_counter
                FROM users WHERE telegram_id = {telegram_id}'''
    result = execute_read_query(query)
    print(result)
    return result


def get_ban_users():
    query = "SELECT * FROM users WHERE ban_status = 1"
    return execute_read_query(query)


def get_file_id(short_id):
    query = "SELECT file_id FROM short_id where id = ?"
    values = (short_id,)
    result = execute_read_query(query, values, bot = "short_id.db")
    return result


def check_shedule_post():
    query = 'SELECT EXISTS(SELECT * FROM sheduler)'
    return execute_read_query(query, bot='sheduler.db')

def get_time_last_post():
    query = "SELECT MAX(send_time) FROM sheduler"
    return execute_read_query(query, bot='sheduler.db')


def get_posts(time):
    query = "SELECT id, file_id, content_type FROM sheduler WHERE send_time <= ?"
    values = (time,)
    return execute_read_query(query, values, bot='sheduler.db')


def get_content_type(short_id):
    query = "SELECT content_type FROM short_id where id = ?"
    values = (short_id,)
    result = execute_read_query(query, values, bot="short_id.db")
    return result


def get_posts_quantity():
    query = 'SELECT COUNT(*) FROM sheduler'
    return execute_read_query(query, bot='sheduler.db')