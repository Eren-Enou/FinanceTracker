import sqlite3
import os

# Define the path to our SQLite database file
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../database/finance_tracker.db')

def create_connection():
    """Create a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        print(e)
    return conn

def add_user(username, password, initial_balance=0):
    """Add a new user to the database."""
    conn = create_connection()
    query = """
    INSERT INTO users(username, password, initial_balance)
    VALUES(?, ?, ?)
    """
    try:
        c = conn.cursor()
        c.execute(query, (username, password, initial_balance))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

def get_user(username):
    """Retrieve a user's details by their username."""
    conn = create_connection()
    query = "SELECT user_id, username, initial_balance FROM users WHERE username = ?"
    try:
        c = conn.cursor()
        c.execute(query, (username,))
        user = c.fetchone()
        return user
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

def update_user(username, new_password=None, new_balance=None):
    """Update a user's details."""
    conn = create_connection()
    if new_password and new_balance:
        query = "UPDATE users SET password = ?, initial_balance = ? WHERE username = ?"
        data = (new_password, new_balance, username)
    elif new_password:
        query = "UPDATE users SET password = ? WHERE username = ?"
        data = (new_password, username)
    elif new_balance:
        query = "UPDATE users SET initial_balance = ? WHERE username = ?"
        data = (new_balance, username)
    else:
        return  # No updates provided

    try:
        c = conn.cursor()
        c.execute(query, data)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
