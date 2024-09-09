import sqlite3

# Создание и подключение к базе данных
conn = sqlite3.connect('school_data.db')
cursor = conn.cursor()

# Создание таблицы students
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    grade TEXT
)
''')

conn.commit()
conn.close()

print("Таблица students успешно создана!")
