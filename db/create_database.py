import sqlite3
import os


def create_database():
    DB_PATH = 'succulentum.db'

    if os.path.exists(DB_PATH):
        response = input("База данных уже существует. Пересоздать? (y/n): ")
        if response.lower() != 'y':
            return -1
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    sql_files = [
        'scripts/create_plants.sql',
        'scripts/create_plant_events.sql'
    ]

    for sql_file in sql_files:
        if os.path.exists(sql_file):
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
                cursor.executescript(sql_script)
        else:
            return -1

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()