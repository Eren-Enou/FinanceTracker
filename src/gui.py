import sys
sys.path.append("..")  # Adds the parent directory to the sys.path

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Toplevel
from database.db_setup import create_connection
from src.transactions import add_transaction, get_transactions, delete_transaction
from src.users import add_user, check_password, get_user_by_username
from src.visualizations import plot_monthly_data, plot_category_data


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(pady=20, padx=20)
        
        self.create_widgets()

    def create_widgets(self):
        # Button to login a user
        self.login_btn = ttk.Button(self.main_frame, text="Login", command=self.login_user)
        self.login_btn.pack(pady=10)

        # Button to register a new user
        self.register_btn = ttk.Button(self.main_frame, text="Register User", command=self.register_user)
        self.register_btn.pack(pady=10)

        # Button to add a new transaction
        # self.transaction_btn = ttk.Button(self.main_frame, text="Add Transaction", command=self.add_new_transaction)
        # self.transaction_btn.pack(pady=10)

    def register_user(self):
    # Connect to the database
        conn = create_connection()
        
        # Simple dialogs to input user details
        username = simpledialog.askstring("Registration", "Enter your username:")
        password = simpledialog.askstring("Registration", "Enter your password:", show="*")
        initial_balance = simpledialog.askfloat("Registration", "Enter your initial balance (optional):", initialvalue=0.0)
        
        # Add user to the database
        if username and password:
            user_id = add_user(conn, username, password, initial_balance)
            messagebox.showinfo("Success", f"User {username} registered successfully with ID {user_id}!")
        else:
            messagebox.showerror("Error", "Username and password are required!")
    
    # initial add new transaction before log in.
    # def add_new_transaction(self):
    #     # Connect to the database
    #     conn = create_connection()

    #     # Simple dialogs to input transaction details
    #     user_id = simpledialog.askinteger("New Transaction", "Enter your user ID:")
    #     trans_type = simpledialog.askstring("New Transaction", "Enter transaction type (income/expense):")

    #     # Based on transaction type, determine the category options
    #     category_options = []
    #     if trans_type == "income":
    #         category_options = ["salary", "freelance income", "rental income", "investments", "gifts", "misc income"]
    #     elif trans_type == "expense":
    #         category_options = ["housing", "food", "transportation", "health", "entertainment", "shopping", "education", "travel", "savings", "loans", "misc"]

    #     # Create a new Toplevel window for category selection
    #     category_window = Toplevel(self.root)
    #     category_window.title("Select Category")
        
    #     ttk.Label(category_window, text="Select Category:").pack(pady=10)
        
    #     category_var = tk.StringVar()
    #     category_combobox = ttk.Combobox(category_window, values=category_options, textvariable=category_var)
    #     category_combobox.pack(pady=10)
    #     category_combobox.set("Choose a category")

    #     ttk.Button(category_window, text="Submit", command=category_window.destroy).pack(pady=10)
    #     category_window.mainloop()

    #     category = category_var.get()

    #     description = simpledialog.askstring("New Transaction", "Enter transaction description:")
    #     amount = simpledialog.askfloat("New Transaction", "Enter transaction amount:")
    #     date = simpledialog.askstring("New Transaction", "Enter transaction date (YYYY-MM-DD):")

    #     # Add transaction to the database
    #     if all([user_id, category, description, amount, date, trans_type]):
    #         add_transaction(conn, user_id, category, description, amount, date, trans_type)
    #         messagebox.showinfo("Success", "Transaction added successfully!")
    #     else:
    #         messagebox.showerror("Error", "Please fill in all fields!")

    def login_user(self):
        # Connect to the database
        conn = create_connection()
        
        # Simple dialogs to input user login details
        username = simpledialog.askstring("Login", "Enter your username:")
        password = simpledialog.askstring("Login", "Enter your password:", show="*")
        
        # Fetch hashed password from the database for the given username
        query = "SELECT password FROM users WHERE username = ?"
        cur = conn.cursor()
        cur.execute(query, (username,))
        result = cur.fetchone()
        
        self.current_username = username
        
        if result:
            hashed_pwd = result[0]
            if check_password(hashed_pwd, password):
                messagebox.showinfo("Success", "Logged in successfully!")
                self.current_username = username
                
                # Destroy the main frame to remove the main interface
                self.main_frame.destroy()

                user = get_user_by_username(conn, username)
                self.show_user_dashboard(user)
            else:
                messagebox.showerror("Error", "Incorrect password!")
        else:
            messagebox.showerror("Error", "Username not found!")

    def show_user_dashboard(self, user):
        """Display the user dashboard."""
        # Check if dashboard_frame exists, if not, create it
        try:
            self.dashboard_frame
        except AttributeError:
            self.dashboard_frame = ttk.Frame(self.root)
            self.dashboard_frame.pack(pady=20, padx=20)
        
        # Clear previous widgets from the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
        
        
        # Display user details
        ttk.Label(self.dashboard_frame, text=f"Welcome, {user[1]}!").pack(pady=10)
        ttk.Label(self.dashboard_frame, text=f"Balance: ${user[3]}").pack(pady=10)

        # Display user transactions
        ttk.Label(self.dashboard_frame, text="Your Transactions:").pack(pady=10)
        transactions = get_transactions(create_connection(), user_id=user[0])

        for transaction in transactions:
            # Create a frame for each transaction
            transaction_frame = ttk.Frame(self.dashboard_frame)
            transaction_frame.pack(pady=5, fill=tk.X, expand=True)

            # Display transaction details within the frame
            ttk.Label(transaction_frame, text=f"${transaction[4]} - {transaction[5]} ({transaction[3]})").pack(side=tk.LEFT)

            # Create a delete button for each transaction and pack it to the right within the frame
            delete_button = ttk.Button(transaction_frame, text="x", command=lambda trans_id=transaction[0]: self.delete_transaction_entry(trans_id))
            delete_button.pack(side=tk.RIGHT)


        # Button to add a new transaction
        self.add_transaction_btn = ttk.Button(self.dashboard_frame, text="Add New Transaction", 
                                            command=lambda: self.dashboard_add_transaction(user[0]))
        self.add_transaction_btn.pack(pady=10)

        # Button to show monthly data
        self.show_monthly_data_btn = ttk.Button(self.dashboard_frame, text="Show Monthly Data", command=lambda: plot_monthly_data(user[0]))
        self.show_monthly_data_btn.pack(pady=10)

        # Button to show category data
        self.show_category_data_btn = ttk.Button(self.dashboard_frame, text="Show Category Data", command=lambda: plot_category_data(user[0]))
        self.show_category_data_btn.pack(pady=10)


    def dashboard_add_transaction(self, user_id):
        """Add a new transaction from the dashboard."""
        # Connect to the database
        conn = create_connection()
        
        # Simple dialogs to input transaction details
        trans_type = simpledialog.askstring("New Transaction", "Enter transaction type (income/expense):")
        
         # Based on transaction type, determine the category options
        category_options = []
        if trans_type == "income":
            category_options = ["salary", "freelance income", "rental income", "investments", "gifts", "misc income"]
        elif trans_type == "expense":
            category_options = ["housing", "food", "transportation", "health", "entertainment", "shopping", "education", "travel", "savings", "loans", "misc"]

        # Create a new Toplevel window for category selection
        category_window = Toplevel(self.root)
        category_window.title("Select Category")
        
        ttk.Label(category_window, text="Select Category:").pack(pady=10)
        
        category_var = tk.StringVar()
        category_combobox = ttk.Combobox(category_window, values=category_options, textvariable=category_var)
        category_combobox.pack(pady=10)
        category_combobox.set("Choose a category")

        ttk.Button(category_window, text="Submit", command=lambda: self._continue_add_transaction(user_id, category_var, category_window, trans_type)).pack(pady=10)

    def _continue_add_transaction(self, user_id, category_var, category_window, trans_type):
        """Continue adding a transaction after the category has been selected."""
        # Close the category selection window
        category_window.destroy()

        # Retrieve the category from the StringVar
        category = category_var.get()

        # Continue with the transaction dialogs
        description = simpledialog.askstring("New Transaction", "Enter transaction description:")
        amount = simpledialog.askfloat("New Transaction", "Enter transaction amount:")
        date = simpledialog.askstring("New Transaction", "Enter transaction date (YYYY-MM-DD):")

        # Connect to the database
        conn = create_connection()

        # Add transaction to the database
        if all([category, description, amount, date, trans_type]):
            add_transaction(conn, user_id, category, description, amount, date, trans_type)
            messagebox.showinfo("Success", "Transaction added successfully!")
            # Refresh the dashboard to reflect the new transaction
            user = get_user_by_username(conn, self.current_username)
            self.show_user_dashboard(user)
        else:
            messagebox.showerror("Error", "Please fill in all fields!")
    
    def delete_transaction_entry(self, transaction_id):
        """Delete a transaction and refresh the dashboard."""
        with create_connection() as conn:
            delete_transaction(conn, transaction_id)
        user = get_user_by_username(create_connection(), self.current_username)
        self.show_user_dashboard(user)


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
