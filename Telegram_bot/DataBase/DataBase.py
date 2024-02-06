import sqlite3


class Telegram_DB:
    def __init__(self):
        self.conn = sqlite3.connect('mbt.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_data (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER NOT NULL,
                access          TEXT    NOT NULL
                                        DEFAULT "Гость",
                data_reg        DATA    NOT NULL,
                user_status     TEXT,
                rating          INTEGER DEFAULT (0),
                profit          INTEGER DEFAULT (0),
                orders          INTEGER DEFAULT (0),
                comment         TEXT,
                photo           BLOB,
                fio             TEXT    NOT NULL,
                sex             TEXT    NOT NULL
                                        CHECK (sex = "Мужской" OR "Женский"),
                born            TEXT    NOT NULL,
                residence_place TEXT,
                education_level TEXT    NOT NULL,
                profession      TEXT,
                work_time_type  TEXT,
                languages       TEXT,
                phone           TEXT    NOT NULL,
                driver          TEXT,
                army            INTEGER,
                add_information TEXT
            )
        ''')
        self.conn.commit()
    
    def add_user(self, user_id, data_reg, fio, sex, born, education_level, profession, phone, add_information):
        self.cursor.execute('''
        INSERT INTO users_data (user_id, data_reg, fio, sex, born, education_level, profession, phone, add_information)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, data_reg, fio, sex, born, education_level, profession, phone, add_information))
        self.conn.commit()
    
    def get_user_info(self, user_id):
        result = self.cursor.execute('''
        SELECT data_reg, profit, orders, fio, sex, born, education_level, profession, phone, add_information FROM users_data
        WHERE user_id = ?
        ''', (user_id, )).fetchone()
        return result
    
    def user_is_exist(self, user_id):
        user = self.cursor.execute('''
        SELECT * FROM users_data
        WHERE user_id = ?
        ''', (user_id, )).fetchone()
        if user is not None:
            return 1
        else:
            return 0
    
    def remove_user(self, user_id):
        try:
            self.cursor.execute('''
            DELETE FROM users_data
            WHERE user_id = ?
            ''', (user_id, ))
            return 1
        except:
            return 0

    def close(self):
        self.conn.close()


class Companies_DB:
    def __init__(self):
        self.conn = sqlite3.connect('mbt.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        # Создаем таблицу, если ее нет
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_state TEXT,
                first_name TEXT,
                last_name TEXT,
                age INTEGER
            )
        ''')
        self.conn.commit()
    
    def add_user(self, user_id, user_state, first_name, last_name, age):
        self.cursor.execute('''
        INSERT INTO telegram_data (user_id, user_state, first_name, last_name, age)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, user_state, first_name, last_name, age))
        self.conn.commit()
        return True
    
    def get_user_data(self, user_id):
        result = self.cursor.execute('''
        SELECT * FROM telegram_data
        WHERE user_id = ?
        ''', (user_id, )).fetchone()
        return result
    
    def close(self):
        self.conn.close()