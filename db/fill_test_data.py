import sqlite3
from pathlib import Path


def fill_test_data():
    current_dir = Path(__file__).parent
    DB_PATH = current_dir / 'succulentum.db'

    if not DB_PATH.exists():
        return -1

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql_script_path = current_dir / 'scripts' / 'fill_test_data.sql'

    if sql_script_path.exists():
        try:
            with open(sql_script_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()

            cursor.executescript(sql_script)

            cursor.execute("SELECT COUNT(*) as count FROM plants")
            plants_count = cursor.fetchone()['count']

            cursor.execute("SELECT COUNT(*) as count FROM plant_events")
            events_count = cursor.fetchone()['count']

            conn.commit()
            conn.close()

            return 0

        except Exception as e:
            conn.rollback()
            conn.close()
            return -1
    else:
        conn.close()
        return -1


if __name__ == "__main__":
    result = fill_test_data()
    if result == 0:
        print("Тестовые данные успешно добавлены!")
    else:
        print("Добавление тестовых данных завершено с ошибками")
