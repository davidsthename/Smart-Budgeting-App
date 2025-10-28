from datetime import datetime


class InvalidTransactionError(Exception):
    """Custom error raised when a transaction is invalid.For example:
    - Negative amount entered
    - Invalid transaction type
    - Wrong date format"""
    pass


class Transaction:
    def __init__(self, date, description, amount, category, t_type):
        """Begins a new transaction
        date: string or datetime showing date of transaction
        description: string describing the transaction
        amount: float showing the amount of transction that occured
        category: string showing the category of the transaction eg 'groceries', 'rent'etc
        t_type: string showing the type of transaction eg 'income' or 'Expense'
        """

        # this make sure the amount is not negative
        if amount < 0:
            raise InvalidTransactionError(
                "Amount cannot be a negative value.")

        t_type = t_type.capitalize()
        # this makes sure the transaction type is valid
        if t_type not in ['Income', 'Expense']:
            raise InvalidTransactionError(
                "Transaction type has to be 'Income' or 'Expense'.")

        # this makes sure the date is a datetime object and also converts string to datetime object
        if isinstance(date, str):
            try:
                date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise InvalidTransactionError(
                    "Date string must be in 'YYYY-MM-DD' format.")

        self.date = date
        self.description = description
        self.amount = amount
        self.category = category
        self.t_type = t_type

    def __str__(self):
        """how the transaction will look when printed eg 2025-02-14 | Groceries | Food | Expense | ₦5,000.00"""
        return f"{self.date.date()} | {self.description} | {self.category} | {self.t_type} | ₦{self.amount:,.2f}"

    def to_dict(self):
        """
       Converts the transaction object into a dictionary.
       Useful when saving to a JSON or CSV file.
       Example:
       {
           "date": "2025-10-23",
           "description": "Salary",
           "amount": 50000.0,
           "category": "Work",
           "type": "Income"
       }
       """
        return {
            # Convert datetime back to string
            "date": self.date.strftime("%Y-%m-%d"),
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "type": self.t_type
        }
