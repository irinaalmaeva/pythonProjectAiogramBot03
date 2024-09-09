import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('school_data.db')
cursor = conn.cursor()

# Выполнение запроса для получения всех данных из таблицы students
cursor.execute('SELECT * FROM students')

# Получение всех строк
rows = cursor.fetchall()

# Печать всех строк
for row in rows:
    print(row)

# Закрытие соединения с базой данных
conn.close()