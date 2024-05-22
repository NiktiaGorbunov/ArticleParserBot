import sqlite3

class SQLighter:

    def __init__(self, database_file):
        #Подключаемся к БД и сохраняем курсор соединения
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
        print("Инициализация базы данных прошла успешно")

    def get_subcriptions(self, status = 'true'):
        #полуачем всех активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM 'subscriptions' WHERE status = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        #Проверяем, есть ли ползьователь в базе
        with self.connection:
            result =  self.cursor.execute("SELECT * FROM 'subscriptions' WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status = 'true'):
        #Добавляем нового пользователя
        with self.connection:
            return self.cursor.execute("INSERT INTO 'subscriptions' ('user_id', 'status') VALUES (?,?)", (user_id, status))

    def update_subcription(self, user_id, status):
        #Обновляем статус пользователя
        with self.connection:
            return self.cursor.execute("UPDATE 'subscriptions' SET 'status' = ? WHERE user_id = ? ", (status,user_id))

    def close(self):
        #Закрываем соединение
        self.connection.close()

