import sqlite3
from pathlib import Path


def create_database():
    current_dir = Path(__file__).parent
    DB_PATH = current_dir / 'succulentum.db'

    print(f"Путь к БД: {DB_PATH}")

    if DB_PATH.exists():
        response = input("База данных уже существует. Пересоздать? (y/n): ")
        if response.lower() != 'y':
            print("Отмена создания базы данных")
            return -1
        print(f"Удаляем существующую БД: {DB_PATH}")
        DB_PATH.unlink()

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    sql_files = [
        current_dir / 'scripts' / 'create_plants.sql',
        current_dir / 'scripts' / 'create_plant_events.sql'
    ]

    for sql_file in sql_files:
        if sql_file.exists():
            try:
                with open(sql_file, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                cursor.executescript(sql_script)
            except Exception as e:
                conn.close()
                return -1
        else:
            conn.close()
            return -1

    conn.commit()
    conn.close()
    return 0


if __name__ == "__main__":
    result = create_database()
    if result == 0:
        print("База данных успешно создана!")
    else:
        print("Создание базы данных завершено с ошибками")