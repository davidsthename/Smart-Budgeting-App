import re
import csv
from transaction import Transaction, InvalidTransactionError


def parse_csv_line(line):
    """
    Cleans and parses a single CSV/receipt line using csv.reader.
    Handles both comma and semicolon separators and quoted fields.
    Example:
      "2025/10/23, Salary, ₦50,000, Work, Income"
      "2025/10/26; Internet Subscription; ₦10,000; Utilities; Expense"
    """
    line = line.strip()
    if not line:
        raise InvalidTransactionError("Empty line.")

    # Convert slashes in dates to dashes
    line = re.sub(r"[\/]", "-", line)

    # Use csv.reader to handle quoted fields and different separators
    try:
        # Try comma separator first
        reader = csv.reader([line], delimiter=',', quotechar='"')
        parts = next(reader)
        if len(parts) != 5:
            # Try semicolon separator
            reader = csv.reader([line], delimiter=';', quotechar='"')
            parts = next(reader)

        parts = [p.strip() for p in parts if p.strip()]
        # print(f"Debug: Parsed parts = {parts}")

        if len(parts) != 5:
            raise InvalidTransactionError(f"Invalid format: {line}")

        date, description, amount, category, t_type = parts

        # Clean and convert amount
        clean_amount = re.sub(r"[₦,\s]", "", amount)

        try:
            clean_amount = float(clean_amount)
        except ValueError:
            raise InvalidTransactionError(f"Invalid amount: {amount}")

        return Transaction(
            date.strip(),
            description.strip(),
            clean_amount,
            category.strip(),
            t_type.strip().capitalize(),
        )
    except Exception as e:
        raise InvalidTransactionError(f"Invalid format: {line} ({str(e)})")
