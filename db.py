import sqlite3
import os

class DBConnection:
	def __init__(self):
		self.conn: sqlite3.Connection | None = None

	def __enter__(self):
		self.conn = sqlite3.connect('database.db')
		self.conn.row_factory = sqlite3.Row
		return self.conn

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.conn.commit()
		self.conn.close()


def insert_post(table, **kwargs):
	pass


def select(table, *args):
	pass

# def delete_user(user_id):
#     with sqlite3.connect('database.db') as conn:
#         cursor = conn.cursor()
#
#         # Шаг 1: Найти все записи, связанные с удаляемым пользователем
#         cursor.execute('''
#             SELECT posts.id, likes.id, files.id
#             FROM users
#             LEFT JOIN posts ON users.id = posts.user_id
#             LEFT JOIN likes ON users.id = likes.user_id
#             LEFT JOIN files ON posts.id = files.post_id
#             WHERE users.id = ?;
#         ''', (user_id,))
#         records = cursor.fetchall()
#
#         # Шаг 2: Удалить записи из таблиц
#         cursor.execute('DELETE FROM likes WHERE user_id = ?', (user_id,))
#         for record in records:
#             if record[0]:  # Проверяем, есть ли записи в таблице posts
#                 cursor.execute('DELETE FROM files WHERE post_id = ?', (record[0],))
#                 cursor.execute('DELETE FROM posts WHERE id = ?', (record[0],))
#
#         # Шаг 3: Удалить пользователя
#         cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
# 	delete_user_files(user_id)
# def delete_user_files(user_id):
#     # Путь к папке с загруженными файлами
#     upload_folder = os.path.join(os.getcwd(), 'static', 'uploads')
#
#     # Получаем список файлов пользователя
#     user_files = get_user_files(user_id)
#
#     # Удаляем каждый файл из папки uploads
#     for filename in user_files:
#         file_path = os.path.join(upload_folder, filename)
#         if os.path.exists(file_path):
#             os.remove(file_path)
#
# def get_user_files(user_id):
#     with sqlite3.connect('database.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute('SELECT music, image FROM files WHERE post_id IN (SELECT id FROM posts WHERE user_id = ?)', (user_id,))
#         files = cursor.fetchall()
#
#     # Собираем список файлов пользователя
#     user_files = [file for sublist in files for file in sublist if file is not None]
#
#     return user_files
def user_exists(username):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
    return user is not None

def create_user(username, password):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))


def create():
	print('creating database')
	with DBConnection() as conn:
		with open('schema.sql', 'r') as file:
			conn.executescript(file.read())


def fill():
	print('filling database')
	with DBConnection() as conn:
		conn.execute('INSERT INTO users (username, password) values (?, ?)', ("asdasd", 'wwwwww'))
		conn.execute('INSERT INTO posts (post_name, content, user_id) values (?, ?, ?)', ("Navalny", 'Navalny umer', 1))
		conn.execute('INSERT INTO profiles (user_id,full_name, bio) values (?, ?, ?)', ("170", "admin", "Я админ"))
