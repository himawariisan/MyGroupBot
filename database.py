import sqlite3
import numpy as np

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            matrix_data TEXT    
        )
    ''')

    conn.commit()
    conn.close()


def save_user_data(user_id: int, name: str, matrix: np.ndarray):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    matrix_str = "".join(map(str, matrix.flatten()))

    cursor.execute('''
        INSERT INTO users (user_id, name, matrix_data)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            name = excluded.name,
            matrix_data=excluded.matrix_data
    ''', (user_id, name, matrix_str))

    conn.commit()
    conn.close()


def get_user_matrix_db(user_id: int) -> np.ndarray:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT matrix_data FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        arr = [int(char) for char in row[0]]
        return np.array(arr).reshape((5, 5))
    else:
        return np.zeros((5, 5), dtype=int)
