import sqlite3
import os

# Define the path to our SQLite database file
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'finance_tracker.db')

def create_connection():
    """Create a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        print(e)
    return conn

def setup_database():
    """Set up the tables for the SQLite database."""
    conn = create_connection()
    if conn:
        create_users_table(conn)
        create_transactions_table(conn)
        conn.close()

def create_users_table(conn):
    """Create the users table in the database."""
    users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        balance REAL DEFAULT 0
    );
    """
    try:
        c = conn.cursor()
        c.execute(users_table_query)
    except sqlite3.Error as e:
        print(e)

def create_transactions_table(conn):
    """Create the transactions table in the database."""
    transactions_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        category TEXT NOT NULL,
        description TEXT,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    );
    """
    try:
        c = conn.cursor()
        c.execute(transactions_table_query)
    except sqlite3.Error as e:
        print(e)

def drop_users_table(database_path):
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    cur.execute("DROP TABLE users;")
    conn.commit()
    conn.close()



if __name__ == '__main__':
    setup_database()
