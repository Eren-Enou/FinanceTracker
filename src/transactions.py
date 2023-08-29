def add_transaction(conn, user_id, category, description, amount, date, trans_type):
    """
    Add a new transaction to the transactions table.
    
    Parameters:
    - conn: SQLite connection object.
    - user_id: ID of the user adding the transaction.
    - category: Category of the transaction (e.g., "Food", "Entertainment").
    - description: Brief description of the transaction.
    - amount: Amount of the transaction.
    - date: Date of the transaction.
    - trans_type: Type of the transaction ('income' or 'expense').
    
    Returns:
    - ID of the newly added transaction.
    """
    query = """
    INSERT INTO transactions(user_id, category, description, amount, date, type)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cur = conn.cursor()
    cur.execute(query, (user_id, category, description, amount, date, trans_type))
    conn.commit()
    return cur.lastrowid

def get_transactions(conn, user_id=None):
    """
    Retrieve transactions from the transactions table.
    
    Parameters:
    - conn: SQLite connection object.
    - user_id (optional): If provided, fetch transactions for this user only.
    
    Returns:
    - List of transactions.
    """
    query = "SELECT * FROM transactions"
    params = ()
    
    if user_id:
        query += " WHERE user_id = ?"
        params = (user_id,)
    
    cur = conn.cursor()
    cur.execute(query, params)
    return cur.fetchall()


def delete_transaction(conn, transaction_id):
    """Delete a transaction by its ID."""
    query = "DELETE FROM transactions WHERE transaction_id = ?"
    cur = conn.cursor()
    cur.execute(query, (transaction_id,))
    conn.commit()


