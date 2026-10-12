
import json
import os
from datetime import date

FILE_NAME = "expenses.json"


def load_expenses():
    """Load saved expenses from the JSON file."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved expenses.")
        return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)
        return True
    except OSError:
        print("Error: Could not save expenses.")
        return False


def add_expense(expenses):
    """Collect and store a new expense."""
    name = input("Enter expense name: ").strip()

    if not name:
        print("Expense name cannot be empty.")
        return

    try:
        amount = float(input("Enter amount (₹): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    category = input(
        "Enter category (Food/Transport/Shopping/Other): "
    ).strip()

    if not category:
        category = "Other"

    expense = {
        "name": name,
        "amount": round(amount, 2),
        "category": category.title(),
        "date": date.today().isoformat()
    }

    expenses.append(expense)

    if save_expenses(expenses):
        print("\nExpense added successfully!")
        print(f"Name: {name}")
        print(f"Amount: ₹{amount:.2f}")
        print(f"Category: {category.title()}")
    else:
        expenses.pop()


def view_expenses(expenses):
    """Display all saved expenses."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n========== ALL EXPENSES ==========")

    for index, expense in enumerate(expenses, start=1):
        print(f"\nExpense #{index}")
        print(f"Name: {expense['name']}")
        print(f"Amount: ₹{expense['amount']:.2f}")
        print(f"Category: {expense['category']}")
        print(f"Date: {expense['date']}")

    print("\n==================================")


def view_total(expenses):
    """Calculate and display total spending."""
    total = sum(expense["amount"] for expense in expenses)

    print("\n========== TOTAL SPENDING ==========")
    print(f"Total expenses: {len(expenses)}")
    print(f"Total amount: ₹{total:.2f}")
    print("====================================")


def view_category_totals(expenses):
    """Calculate spending for each category."""
    if not expenses:
        print("\nNo expenses available.")
        return

    totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category not in totals:
            totals[category] = 0

        totals[category] += amount

    print("\n======= SPENDING BY CATEGORY =======")

    for category, amount in sorted(totals.items()):
        print(f"{category}: ₹{amount:.2f}")

    print("====================================")


def delete_expense(expenses):
    """Delete an expense by its displayed number."""
    if not expenses:
        print("\nNo expenses to delete.")
        return

    view_expenses(expenses)

    try:
        number = int(input("\nEnter expense number to delete: "))

        if number < 1 or number > len(expenses):
            print("Invalid expense number.")
            return

    except ValueError:
        print("Please enter a valid whole number.")
        return

    removed = expenses.pop(number - 1)

    if save_expenses(expenses):
        print(f"Deleted expense: {removed['name']}")
    else:
        expenses.insert(number - 1, removed)


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 36)
    print("       PERSONAL EXPENSE TRACKER")
    print("=" * 36)
    print("1. Add an expense")
    print("2. View all expenses")
    print("3. View total spending")
    print("4. View spending by category")
    print("5. Delete an expense")
    print("6. Exit")
    print("=" * 36)


def main():
    """Run the application."""
    expenses = load_expenses()

    print("Welcome to your Personal Expense Tracker!")

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            view_total(expenses)

        elif choice == "4":
            view_category_totals(expenses)

        elif choice == "5":
            delete_expense(expenses)

        elif choice == "6":
            print("Thank you for using Expense Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()