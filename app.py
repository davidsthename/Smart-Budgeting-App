import tkinter as tk
from tkinter import ttk, messagebox
from account import Account
from transaction import Transaction
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Create an Account instance
my_account = Account("David")
my_account.load_from_csv("transactions_data.csv")

# Create the main window
root = tk.Tk()
root.title("Smart Budgeting App")
root.geometry("700x550")
root.config(bg="#f4f4f4")

# ==== Title ====
title_label = tk.Label(root, text="Smart Budgeting App",
                       font=("Arial", 18, "bold"), bg="#f4f4f4")
title_label.pack(pady=10)

# ==== Frame for form inputs ====
form_frame = tk.Frame(root, bg="#f4f4f4")
form_frame.pack(pady=10)

# Date
tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="#f4f4f4").grid(
    row=0, column=0, padx=5, pady=5, sticky="e")
date_entry = tk.Entry(form_frame, width=30)
date_entry.grid(row=0, column=1, padx=5, pady=5)

# Description
tk.Label(form_frame, text="Description:", bg="#f4f4f4").grid(
    row=1, column=0, padx=5, pady=5, sticky="e")
desc_entry = tk.Entry(form_frame, width=30)
desc_entry.grid(row=1, column=1, padx=5, pady=5)

# Amount
tk.Label(form_frame, text="Amount (₦):", bg="#f4f4f4").grid(
    row=2, column=0, padx=5, pady=5, sticky="e")
amount_entry = tk.Entry(form_frame, width=30)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

# Category
tk.Label(form_frame, text="Category:", bg="#f4f4f4").grid(
    row=3, column=0, padx=5, pady=5, sticky="e")
category_entry = tk.Entry(form_frame, width=30)
category_entry.grid(row=3, column=1, padx=5, pady=5)

# Type (Income / Expense)
tk.Label(form_frame, text="Type:", bg="#f4f4f4").grid(
    row=4, column=0, padx=5, pady=5, sticky="e")
type_var = tk.StringVar(value="Expense")
tk.Radiobutton(form_frame, text="Income", variable=type_var,
               value="Income", bg="#f4f4f4").grid(row=4, column=1, sticky="w")
tk.Radiobutton(form_frame, text="Expense", variable=type_var,
               value="Expense", bg="#f4f4f4").grid(row=4, column=1, sticky="e")

# ==== Add Transaction Button ====
add_button = tk.Button(root, text="Add Transaction", bg="#0078D7",
                       fg="white", width=20, font=("Arial", 10, "bold"),
                       command=lambda: add_transaction())
add_button.pack(pady=10)

# ==== Listbox for transaction list ====
transactions_list = tk.Listbox(root, width=80, height=12)
transactions_list.pack(pady=10)

# ==== Dashboard Summary ====
summary_frame = tk.Frame(root, bg="#f4f4f4")
summary_frame.pack(pady=10)

income_label = tk.Label(summary_frame, text="Income: ₦0.00",
                        font=("Arial", 10, "bold"), bg="#f4f4f4", fg="green")
income_label.grid(row=0, column=0, padx=15)

expense_label = tk.Label(summary_frame, text="Expense: ₦0.00",
                         font=("Arial", 10, "bold"), bg="#f4f4f4", fg="red")
expense_label.grid(row=0, column=1, padx=15)

balance_label = tk.Label(summary_frame, text="Balance: ₦0.00",
                         font=("Arial", 10, "bold"), bg="#f4f4f4", fg="#0078D7")
balance_label.grid(row=0, column=2, padx=15)


# === Function to add a transaction ===
def add_transaction():
    date = date_entry.get()
    description = desc_entry.get()
    amount = amount_entry.get()
    category = category_entry.get()
    t_type = type_var.get()

    if not (date and description and amount and category and t_type):
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number.")
        return

    try:
        transaction = Transaction(date, description, amount, category, t_type)
        my_account.add_transaction(transaction)
        my_account.save_to_csv("transactions_data.csv")
        messagebox.showinfo(
            "Success", f"✅ Transaction added: {description} ({t_type}) ₦{amount:,.2f}")
        update_transaction_list()
        update_summary()
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def update_summary():
    total_income = my_account.total_income()
    total_expense = my_account.total_expense()
    balance = my_account.balance()

    income_label.config(text=f"Income: ₦{total_income:,.2f}")
    expense_label.config(text=f"Expense: ₦{total_expense:,.2f}")
    balance_label.config(text=f"Balance: ₦{balance:,.2f}")


def clear_fields():
    date_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    type_var.set("Expense")


def update_transaction_list():
    transactions_list.delete(0, tk.END)
    for i, txn in enumerate(my_account.transactions):
        transactions_list.insert(
            tk.END, f"{i+1}. {txn.date} | {txn.description} | {txn.category} | {txn.t_type} | ₦{txn.amount:,.2f}")

# displays a pie chart of expenses by category


# def show_pie_chart():
    # df = pd.read_csv("transactions_data.csv")
    # category_totals = df.groupby("category")["amount"].sum()
    # fig, ax = plt.subplots()
    # ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%")
    # canvas = FigureCanvasTkAgg(fig, master=root)
    # canvas.get_tk_widget().pack()
    # canvas.draw()

# displays a bar chart of monthly expenses


# def show_bar_chart():
    # df = pd.read_csv("transactions_data.csv")

    # # Ensure required columns exist
    # if "date" not in df.columns or "amount" not in df.columns:
    #     messagebox.showerror("Error", "Missing required columns in CSV.")
    #     return

    # # Convert date column to datetime and extract month
    # df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # df["month"] = df["date"].dt.strftime("%b %Y")  # Example: Oct 2025

    # # Group total expense by month
    # monthly_expense = df[df["type"] == "Expense"].groupby("month")[
    #     "amount"].sum()

    # if monthly_expense.empty:
    #     messagebox.showinfo(
    #         "No Data", "No expense data available for bar chart.")
    #     return

    # # Create and display bar chart
    # fig, ax = plt.subplots(figsize=(5, 4))
    # monthly_expense.plot(kind="bar", color="#0078D7", ax=ax)
    # ax.set_title("Monthly Expenses", fontsize=12, fontweight="bold")
    # ax.set_ylabel("Amount (₦)")
    # ax.set_xlabel("Month")
    # plt.xticks(rotation=45, ha="right")

    # # Embed in Tkinter
    # canvas = FigureCanvasTkAgg(fig, master=root)
    # canvas.get_tk_widget().pack()
    # canvas.draw()


# === Global variable to track current chart ===
current_chart_canvas = None
current_chart_type = None


def clear_chart():
    """Remove the current chart from the window (if any)."""
    global current_chart_canvas, current_chart_type
    if current_chart_canvas is not None:
        current_chart_canvas.get_tk_widget().pack_forget()
        current_chart_canvas = None
        current_chart_type = None


def show_pie_chart():
    """Toggle the pie chart display."""
    global current_chart_canvas, current_chart_type

    # If pie chart is already showing, hide it
    if current_chart_type == "pie":
        clear_chart()
        return

    # Otherwise, clear old chart and show pie chart
    clear_chart()

    df = pd.read_csv("transactions_data.csv")
    if "category" not in df.columns or "amount" not in df.columns:
        messagebox.showerror("Error", "Missing required columns in CSV.")
        return

    category_totals = df.groupby("category")["amount"].sum()
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie(category_totals, labels=category_totals.index,
           autopct="%1.1f%%", startangle=90)
    ax.set_title("Spending by Category")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()

    current_chart_canvas = canvas
    current_chart_type = "pie"


def show_bar_chart():
    """Toggle the bar chart display."""
    global current_chart_canvas, current_chart_type

    # If bar chart is already showing, hide it
    if current_chart_type == "bar":
        clear_chart()
        return

    # Otherwise, clear old chart and show bar chart
    clear_chart()

    df = pd.read_csv("transactions_data.csv")
    if "date" not in df.columns or "amount" not in df.columns:
        messagebox.showerror("Error", "Missing required columns in CSV.")
        return

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["month"] = df["date"].dt.strftime("%b %Y")

    monthly_expense = df[df["type"] == "Expense"].groupby("month")[
        "amount"].sum()
    if monthly_expense.empty:
        messagebox.showinfo(
            "No Data", "No expense data available for bar chart.")
        return

    fig, ax = plt.subplots(figsize=(5, 4))
    monthly_expense.plot(kind="bar", color="#0078D7", ax=ax)
    ax.set_title("Monthly Expenses", fontsize=12, fontweight="bold")
    ax.set_ylabel("Amount (₦)")
    ax.set_xlabel("Month")
    plt.xticks(rotation=45, ha="right")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()

    current_chart_canvas = canvas
    current_chart_type = "bar"


# This line will show the pie chart button
pie_chart_button = tk.Button(root, text="Show Pie Chart", bg="#0078D7",
                             fg="white", width=20, font=("Arial", 10, "bold"), command=show_pie_chart)
pie_chart_button.pack(pady=10)

bar_chart_button = tk.Button(root, text="Show Bar Chart", bg="#28a745",
                             fg="white", width=20, font=("Arial", 10, "bold"),
                             command=show_bar_chart)
bar_chart_button.pack(pady=5)


# this updates the transaction list on startup
update_transaction_list()
# this updates the summary on startup
update_summary()
# this Runs the Tkinter event loop
root.mainloop()
