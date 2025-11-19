import sqlite3
import os


def create_database():
    DB_PATH = 'succulentum.db'

    if os.path.exists(DB_PATH):
        response = input("База данных уже существует. Пересоздать? (y/n): ")
        if response.lower() != 'y':
            return
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    sql_script_paths = ['scripts/create_plants.sql',
                        'scripts/create_plant_events.sql',
                        'scripts/create_plant_health_checks.sql']

    for script_path in sql_script_paths:
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
                cursor.executescript(sql_script)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
