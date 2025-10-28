from transaction import Transaction, InvalidTransactionError
from csv_importer import parse_csv_line
import csv
import os


class Account:
    """
    The Account class represents a user's wallet or financial record.
    It stores multiple Transaction objects and provides useful methods
    for managing them (add, remove, list, calculate totals, etc.)
    """

    def __init__(self, name):
        """Creates a new account with a name (string) and an empty list of transactions."""
        self.name = name
        self.transactions = []  # List to store all Transaction objects

    def add_transaction(self, transaction):
        """
        Adds a new Transaction object to the account.
        Raises TypeError if the provided object is not a Transaction.
        """
        if not isinstance(transaction, Transaction):
            raise TypeError("Only Transaction objects can be added.")

        self.transactions.append(transaction)
        print(
            f"✅ Transaction added: {transaction.description} ({transaction.t_type}) ₦{transaction.amount:,.2f}"
        )

    def remove_transaction(self, index):
        """
        Removes a transaction using its position (index) in the list.
        Handles invalid index errors gracefully.
        """
        try:
            removed = self.transactions.pop(index)
            print(
                f"🗑️ Transaction removed: {removed.description} ({removed.t_type}) ₦{removed.amount:,.2f}"
            )
        except IndexError:
            print("❌ Invalid index. No transaction removed.")

    def list_transactions(self):
        """Prints all transactions in the account."""
        if not self.transactions:
            print("No transaction found.")
            return

        print(f"Transactions for account: {self.name}")
        # get both index and transaction object
        for i, t in enumerate(self.transactions):
            print(f"{i}. {t}")  # This uses Transaction.__str__()

    def total_income(self):
        """Calculates and returns the total income from all transactions."""
        return sum(t.amount for t in self.transactions if t.t_type == "Income")

    def total_expense(self):
        """Calculates and returns the total expense from all transactions."""
        return sum(t.amount for t in self.transactions if t.t_type == "Expense")

    def balance(self):
        """
        Calculates the account balance:
        Balance = Total Income - Total Expense
        """
        return self.total_income() - self.total_expense()

    def category_summary(self, budget=None):
        # Summarizes expenses by category. If a Budget object is provided, also shows remaining budget status.
        category_totals = {}
        for t in self.transactions:
            if t.t_type == "Expense":
                category_totals[t.category] = category_totals.get(
                    t.category, 0) + t.amount

        if not category_totals:
            print("No expense transactions found.")
            return

        print(f"\n📊 Category Spending Summary for '{self.name}':")
        for category, spent in category_totals.items():
            print(f"- {category}: ₦{spent:,.2f}", end="")
            if budget:
                print(f" → {budget.status(category, spent)}")
            else:
                print()

    # account.py (add this method)

    def import_csv(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    if not line.strip() or "date" in line.lower():
                        continue  # skip empty lines or headers
                    try:
                        transaction = parse_csv_line(line)
                        self.add_transaction(transaction)
                    except Exception as e:
                        print(f"⚠️ Skipped invalid line: {line.strip()} ({e})")
            print(f"✅ Finished importing transactions from {filename}")
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found.")

    def save_to_csv(self, filename="transactions_data.csv"):
        """Saves all current transactions to a CSV file."""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["date", "description", "amount", "category", "type"])
            for t in self.transactions:
                writer.writerow([
                    t.date.strftime("%Y-%m-%d"),
                    t.description,
                    t.amount,
                    t.category,
                    t.t_type
                ])
        print(f"💾 Transactions saved to {filename}")

    def load_from_csv(self, filename="transactions_data.csv"):
        """Loads transactions from a CSV file (if it exists)."""
        if not os.path.exists(filename):
            print("⚠️ No saved transaction file found yet.")
            return

        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    transaction = Transaction(
                        row["date"],
                        row["description"],
                        float(row["amount"]),
                        row["category"],
                        row["type"]
                    )
                    self.transactions.append(transaction)
                except Exception as e:
                    print(f"⚠️ Skipped invalid row: {row} ({e})")

        print(
            f"✅ Loaded {len(self.transactions)} transactions from {filename}")
