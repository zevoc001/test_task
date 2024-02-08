import sqlite3


class Telegram_DB:
    def __init__(self):
        self.conn = sqlite3.connect('mbt.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_data (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                Телеграм_ID         INTEGER NOT NULL,
                Доступ          TEXT    NOT NULL
                                        DEFAULT "Гость",
                Дата регистрации        DATA    NOT NULL,
                Статус     TEXT,
                Рейтинг          INTEGER DEFAULT (0),
                Заработок          INTEGER DEFAULT (0),
                Заказы          INTEGER DEFAULT (0),
                Комментарии         TEXT,
                Фотография           BLOB,
                ФИО             TEXT    NOT NULL,
                Пол             TEXT    NOT NULL
                                        CHECK (sex = "Мужской" OR "Женский"),
                Дата рождения            TEXT    NOT NULL,
                Возраст
                Место жительства TEXT,
                Образование TEXT    NOT NULL,
                Специальность      TEXT,
                Рабочее время  TEXT,
                Языки       TEXT,
                Телефон           TEXT    NOT NULL,
                Водительские права          TEXT,
                Машина
                Служил            INTEGER,
                Доп. инф. TEXT
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