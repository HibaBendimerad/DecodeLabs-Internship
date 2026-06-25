# To-Do List Manager

A command-line To-Do List application built in Python as part of the DecodeLabs Industrial Training Kit (Python Programming track, Project 1).

## Overview

This project goes beyond a simple in-memory list. It follows the **IPO model** (Input → Process → Output) and uses **JSON serialization** to persist tasks on disk, so the to-do list survives between program runs — just like a real backend application would handle data storage.

## Features

- Two interfaces available: a command-line menu and a graphical (Tkinter) window
- Add new tasks to the list
- View all tasks with their completion status
- Mark tasks as done (toggle in the GUI version)
- Delete tasks (GUI version)
- Persistent storage using a `tasks.json` file (tasks are not lost when the program closes)
- Clean separation of concerns: data logic (load/save/add/view) vs. user interface (menu/input or window/buttons)

## Concepts Used

| Concept | Where it's used |
|---|---|
| Lists | Storing the collection of tasks |
| Dictionaries | Representing each task (id, task name, done status) |
| `enumerate()` | Displaying tasks with both index and value |
| JSON serialization | Saving/loading tasks to/from `tasks.json` |
| Tkinter (GUI) | Building a graphical window with widgets and event-driven callbacks |
| `if __name__ == "__main__":` | Ensuring the program only runs when executed directly |
| Functions | Splitting logic into reusable, single-responsibility blocks |

## How to Run

### Command-line version
```bash
python3 todo.py
```

You'll see a menu with 4 options:
1. Add a task
2. View all tasks
3. Mark a task as done
4. Exit

### Graphical version (GUI)
```bash
python3 todo_gui.py
```

A window opens where you can type a task and press **Add** (or Enter), select a task and click **Toggle Done** or **Delete**. Both versions share the exact same data logic and the same `tasks.json` file, so they stay in sync.

> Note: on Linux, Tkinter may need to be installed separately with `sudo apt install python3-tk`. It is already included on Windows and macOS.

## Project Structure

```
todo-list-project/
│── todo.py         # Command-line version
│── todo_gui.py     # Graphical version (Tkinter)
│── tasks.json      # Auto-generated file storing your tasks (created on first run)
└── README.md       # Project documentation
```

## Author

Built as part of the DecodeLabs Python Programming Internship — Batch 2026.