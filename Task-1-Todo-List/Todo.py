"""
Project 1: The To-Do List
DecodeLabs Industrial Training Kit - Python Programming

This program manages a list of tasks using the IPO model:
- Input: the user enters a new task
- Process: the task is stored as a dictionary inside a list
- Output: the list of tasks is displayed back to the user

Data persistence is handled through JSON serialization, so tasks
are saved to disk and survive after the program closes.
"""

import json
import os

DATA_FILE = "tasks.json"


def load_tasks():
    """
    Load tasks from the JSON file on disk (Storage -> Memory).
    If the file doesn't exist yet, return an empty list instead
    of crashing the program.
    """
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # File exists but is empty or corrupted
            return []


def save_tasks(tasks):
    """
    Save the current list of tasks to the JSON file (Memory -> Storage).
    This is what makes the data persistent between program runs.
    """
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task(tasks, task_name):
    """
    Process step: create a new task as a dictionary and append it
    to the tasks list. Each task gets a unique id based on its
    position, mimicking a primary key in a database table.
    """
    new_task = {
        "id": len(tasks) + 1,
        "task": task_name,
        "done": False
    }
    tasks.append(new_task)
    return tasks


def view_tasks(tasks):
    """
    Output step: display every task in the list using enumerate(),
    which gives simultaneous access to the index and the value.
    """
    if not tasks:
        print("\nYour to-do list is empty. Add a task to get started!\n")
        return

    print("\n--- YOUR TO-DO LIST ---")
    for index, task in enumerate(tasks, start=1):
        status = "[DONE]" if task["done"] else "[ ]"
        print(f"{index}. {status} {task['task']}")
    print("------------------------\n")


def mark_task_done(tasks, task_id):
    """
    Process step: find a task by its id and mark it as completed.
    """
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return True
    return False


def show_menu():
    """
    Display the available actions to the user (Input step preparation).
    """
    print("=== TO-DO LIST MANAGER ===")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Mark a task as done")
    print("4. Exit")


def main():
    """
    Main program loop. Loads existing tasks at startup, then keeps
    asking the user for actions until they choose to exit.
    """
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            task_name = input("Enter the new task: ").strip()
            if task_name:
                tasks = add_task(tasks, task_name)
                save_tasks(tasks)
                print(f'Task "{task_name}" added successfully!\n')
            else:
                print("Task cannot be empty.\n")

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            view_tasks(tasks)
            try:
                task_id = int(input("Enter the task number to mark as done: ").strip())
                if mark_task_done(tasks, task_id):
                    save_tasks(tasks)
                    print("Task marked as done!\n")
                else:
                    print("Task not found.\n")
            except ValueError:
                print("Please enter a valid number.\n")

        elif choice == "4":
            print("Goodbye! Your tasks have been saved.")
            break

        else:
            print("Invalid option, please choose between 1 and 4.\n")


if __name__ == "__main__":
    main()