import sqlite3
from flask import Flask, url_for, request, render_template, redirect


app = Flask(__name__)


class DB:
    def __init__(self):
        conn = sqlite3.connect('news.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash) 
                          VALUES (?,?)''', (user_name, password_hash))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def clean(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users")
        cursor.close()
        self.connection.commit()


class NewsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (title, content, user_id) 
                          VALUES (?,?,?)''', (title, content, str(user_id)))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(news_id)))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM news WHERE user_id = ?",
                           (str(user_id)))
        else:
            cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id)))
        cursor.close()
        self.connection.commit()

    def clean(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM news")
        cursor.close()
        self.connection.commit()


class User:
    def __init__(self, login, password, model):
        self.model = model
        self.login = login
        self.password = password
        self.model.insert(login, password)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        login = request.form.get('login')
        print(login)
        user_password = request.form.get('login')
        print(user_password)
        if users.exists(login, user_password):
            return redirect('/feed')


@app.route('/feed', methods=['POST', 'GET'])
def feed():
    if request.method == 'GET':
        cur_user_news = news.get_all(user_id=85)
        return render_template('feed.html', news=cur_user_news)
    elif request.method == 'POST':
        pass


if __name__ == '__main__':
    database = DB()
    users = UsersModel(database.get_connection())
    # users.init_table()
    # users.clean()
    # users.insert('Andrey', '12345678')
    # users.insert('ProGamer', '13371212')
    # users.insert('Nastenka', 'qwerty')
    print(users.get_all())

    news = NewsModel(database.get_connection())
    # news.init_table()
    # news.clean()
    news.insert('Вред сотовых телефонов', 'Сотовые телефоны вредны', 85)
    news.insert('Вред сотовых телефо1нов', 'Сотовые те1лефоны вредны', 85)
    news.insert('Вред сот11овых телефонов', 'Сотовые телефо11ны вредны', 85)
    app.run(port=8000, host='127.0.0.1')

