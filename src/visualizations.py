import sys
sys.path.append("..")  # Adds the parent directory to the sys.path

import matplotlib.pyplot as plt

from transactions import get_transactions
from database.db_setup import create_connection

def plot_monthly_data(user_id):
    conn = create_connection()
    transactions = get_transactions(conn, user_id=user_id)
    conn.close()

    # Categorize data by month and type (income/expense)
    monthly_data = {}
    for trans in transactions:
        month = trans[5][:7]  # YYYY-MM format
        if month not in monthly_data:
            monthly_data[month] = {"income": 0, "expense": 0}
        monthly_data[month][trans[6]] += trans[4]

    # Extract data for plotting
    months = sorted(monthly_data.keys())
    income_vals = [monthly_data[month]["income"] for month in months]
    expense_vals = [monthly_data[month]["expense"] for month in months]

    # Plot
    bar_width = 0.35
    r1 = range(len(income_vals))
    r2 = [x + bar_width for x in r1]

    plt.bar(r1, income_vals, width=bar_width, color='b', label='Income')
    plt.bar(r2, expense_vals, width=bar_width, color='r', label='Expense')
    
    plt.xlabel('Month', fontweight='bold')
    plt.xticks([r + bar_width for r in range(len(income_vals))], months)
    plt.ylabel('Amount')
    plt.title('Monthly Income and Expense')
    plt.legend()
    plt.show()

def plot_category_data(user_id):
    conn = create_connection()
    transactions = get_transactions(conn, user_id=user_id)
    conn.close()

    # Categorize data by transaction type
    category_data = {}
    for trans in transactions:
        if trans[2] not in category_data:
            category_data[trans[2]] = 0
        category_data[trans[2]] += trans[4]

    # Extract data for plotting
    categories = category_data.keys()
    amounts = category_data.values()

    # Plot
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Expenditure by Category')
    plt.show()
