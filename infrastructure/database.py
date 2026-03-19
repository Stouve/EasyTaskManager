import sqlite3

def get_connection(db_path:str = "tasks.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory=sqlite3.Row

    return conn

def init_db(db_path: str = "tasks.db"):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()
