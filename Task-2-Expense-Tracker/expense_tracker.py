"""
Project 2: Expense Tracker (CLI Version)
DecodeLabs Industrial Training Kit - Python Programming

This program tracks expenses entered by the user.
It applies the IPO model:
- Input    : user enters an expense amount and a category
- Process  : the accumulator adds it to the running total
- Output   : summary showing all expenses and the final total

Key concepts: accumulators, type conversion (float),
              try/except, sentinel value, JSON persistence.
"""

import json
import os

DATA_FILE = "expenses.json"


# ---------------------------------------------------------------
# DATA LOGIC
# ---------------------------------------------------------------

def load_expenses():
    """Load expenses from the JSON file on disk (Storage -> Memory)."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_expenses(expenses):
    """Save the current list of expenses to the JSON file (Memory -> Storage)."""
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense(expenses, amount, category, description):
    """
    Process step: create a new expense dictionary and append it.
    The accumulator pattern happens at display time via sum().
    """
    new_expense = {
        "id":          len(expenses) + 1,
        "amount":      round(amount, 2),
        "category":    category,
        "description": description
    }
    expenses.append(new_expense)
    return expenses


def compute_total(expenses):
    """
    The accumulator: sum all amounts in the expenses list.
    Equivalent to: total = 0; for e in expenses: total += e["amount"]
    """
    return round(sum(e["amount"] for e in expenses), 2)


def compute_by_category(expenses):
    """Group and sum expenses by category."""
    totals = {}
    for e in expenses:
        cat = e["category"]
        totals[cat] = round(totals.get(cat, 0) + e["amount"], 2)
    return totals


def view_expenses(expenses):
    """Output step: display all expenses and the running total."""
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    print("\n--- EXPENSE REPORT ---")
    for e in expenses:
        print(f"  {e['id']:>2}. [{e['category']:<12}]  "
              f"${e['amount']:>8.2f}  —  {e['description']}")

    print("  " + "-" * 44)
    print(f"  TOTAL SPENT : ${compute_total(expenses):>8.2f}")

    print("\n  By category:")
    for cat, total in compute_by_category(expenses).items():
        print(f"    {cat:<12} : ${total:.2f}")
    print()


# ---------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------

CATEGORIES = ["Food", "Transport", "Shopping", "Health", "Other"]


def show_menu():
    print("=== EXPENSE TRACKER ===")
    print("1. Add an expense")
    print("2. View all expenses")
    print("3. Reset all expenses")
    print("4. Exit")


def main():
    expenses = load_expenses()

    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            # --- INPUT: get amount (with type conversion + error handling) ---
            try:
                amount = float(input("Enter amount ($): ").strip())
                if amount <= 0:
                    print("Amount must be greater than zero.\n")
                    continue
            except ValueError:
                # DEFENSIVE CODING: catch invalid input instead of crashing
                print("Invalid amount. Please enter a number (e.g. 12.50).\n")
                continue

            # --- INPUT: get category ---
            print("Categories: " + ", ".join(
                f"{i+1}.{c}" for i, c in enumerate(CATEGORIES)))
            cat_input = input("Choose category (1-5): ").strip()
            try:
                category = CATEGORIES[int(cat_input) - 1]
            except (ValueError, IndexError):
                category = "Other"

            description = input("Description (optional): ").strip() or "—"

            # --- PROCESS: accumulate ---
            expenses = add_expense(expenses, amount, category, description)
            save_expenses(expenses)
            print(f"\n✔ Expense of ${amount:.2f} added! "
                  f"Running total: ${compute_total(expenses):.2f}\n")

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            confirm = input("Reset ALL expenses? (yes/no): ").strip().lower()
            if confirm == "yes":
                expenses = []
                save_expenses(expenses)
                print("All expenses have been reset.\n")

        elif choice == "4":
            # SENTINEL / KILL SWITCH: graceful shutdown
            print(f"\nGoodbye! Total spent this session: "
                  f"${compute_total(expenses):.2f}")
            break

        else:
            print("Invalid option. Please choose between 1 and 4.\n")


if __name__ == "__main__":
    main()