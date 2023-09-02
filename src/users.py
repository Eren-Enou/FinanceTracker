import sqlite3
import bcrypt

def hash_password(password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def add_user(conn, username, password, balance=0.0):
    """
    Add a new user to the users table.
    
    Parameters:
    - conn: SQLite connection object.
    - username: Username of the new user.
    - password: Password for the new user (will be hashed before storing).
    - balance: Initial balance for the user. Default is 0.0.
    
    Returns:
    - ID of the newly added user.
    """
    hashed_pwd = hash_password(password)
    query = """
    INSERT INTO users(username, password, balance)
    VALUES (?, ?, ?)
    """
    cur = conn.cursor()
    cur.execute(query, (username, hashed_pwd, balance))
    conn.commit()
    return cur.lastrowid

def check_password(hashed_password, user_password):
    """
    Check a password against the hashed version.

    Parameters:
    - hashed_password: The hashed version from the database.
    - user_password: The password provided by the user during login.

    Returns:
    - True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

def get_user_by_username(conn, username):
    """Fetch user details by username."""
    query = "SELECT * FROM users WHERE username = ?"
    cur = conn.cursor()
    cur.execute(query, (username,))
    return cur.fetchone()

def adjust_user_balance(conn, user_id, amount, trans_type):
    """
    Adjust the user's balance based on a transaction.

    Parameters:
    - conn: the database connection object.
    - user_id: the ID of the user whose balance needs adjustment.
    - amount: the amount of the transaction.
    - trans_type: type of transaction ('income' or 'expense').
    """
    cur = conn.cursor()
    
    if trans_type == "income":
        cur.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    elif trans_type == "expense":
        cur.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, user_id))

    conn.commit()

def delete_user(conn, user_id):
    """
    Delete a user from the database based on their user_id.

    Parameters:
    - conn: the database connection object.
    - user_id: the ID of the user to be deleted.
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
