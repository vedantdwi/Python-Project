import json
import os
from collections import defaultdict

# Function to load expense data from file
def load_expenses(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return defaultdict(list)

# Function to save expense data to file
def save_expenses(expenses, file_path):
    with open(file_path, 'w') as file:
        json.dump(expenses, file)

# Function to add a new expense
def add_expense(expenses):
    category = input("Enter expense category: ")
    amount = float(input("Enter expense amount: "))
    description = input("Enter expense description: ")
    expenses[category].append({"amount": amount, "description": description})
    print("Expense added successfully!")

# Function to view monthly expense summary
def view_monthly_summary(expenses):
    for category, category_expenses in expenses.items():
        total_amount = sum(expense['amount'] for expense in category_expenses)
        print(f"{category}: ${total_amount:.2f}")

# Function to view category-wise expenditure
def view_category_expenditure(expenses):
    category = input("Enter category to view expenditure: ")
    if category in expenses:
        for expense in expenses[category]:
            print(f"Amount: ${expense['amount']:.2f}, Description: {expense['description']}")
    else:
        print("No expenses found for this category.")

# Main function
def main():
    file_path = "expenses.json"
    expenses = load_expenses(file_path)

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Monthly Summary")
        print("3. View Category-wise Expenditure")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_monthly_summary(expenses)
        elif choice == '3':
            view_category_expenditure(expenses)
        elif choice == '4':
            save_expenses(expenses, file_path)
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
