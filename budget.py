class Budget:
    """The Budget class manages spending limits for each category.
    It allows users to set, update, and check remaining budget amounts."""

    def __init__(self):
        # creates an empty dictionary to store budget by category
        self.categories = {}  # eg. {"transport": 1000 etc}

    def set_budget(self, category, amount):
        """sets and updates the budget for a specific category"""

        if not isinstance(category, str):
            raise TypeError("Category name must be a string.")
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Budget amount must be a positive number.")

        self.categories[category] = amount
        print(f"Buget set: {category} -> ₦{amount:,.2f}")

    def get_budget(self, category):
        # this returns the budget amount for a specific category if none is fount it returns 0.
        return self.categories.get(category, 0)

    def remaining(self, category, total_spent):
        """
        Calculates how much budget remains for a given category.
        If category doesn’t exist, returns None.
        """
        if category not in self.categories:
            print(f"⚠️ No budget set for category '{category}'.")
            return None

        remaining_amount = self.categories[category] - total_spent
        return remaining_amount

    def status(self, category, total_spent):
        """
        Returns a message showing whether spending is within or over budget.
        """
        remaining = self.remaining(category, total_spent)
        if remaining is None:
            return f"⚠️ No budget set for {category}."

        if remaining >= 0:
            return f"🟢 Within budget. Remaining: ₦{remaining:,.2f}"
        else:
            return f"🔴 Over budget by ₦{abs(remaining):,.2f}"

    def show_all_budgets(self):
        """Prints all budgets and their limits."""
        if not self.categories:
            print("No budgets set yet.")
            return
        print("📋 All Budgets:")
        for cat, amt in self.categories.items():
            print(f"- {cat}: ₦{amt:,.2f}")
