import sqlite3
import os


def seed_database():
    DB_PATH = 'succulentum.db'

    if not os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql_script_path = 'scripts/fill_test_data.sql'

    if os.path.exists(sql_script_path):
        with open(sql_script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            cursor.executescript(sql_script)

    conn.commit()


if __name__ == "__main__":
    seed_database()