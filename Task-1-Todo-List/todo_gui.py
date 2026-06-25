"""
Project 1: The To-Do List (GUI Version - Planner Design)
DecodeLabs Industrial Training Kit - Python Programming
"""

import json
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "tasks.json"

# ---------------------------------------------------------------
# COLOUR PALETTE 
# ---------------------------------------------------------------
BG_CREAM    = "#FAF6EE"#main background (cream/off-white)
CORAL_RED   = "#E8502A"#title and accent color (orange-red)
NAVY        = "#2D3A8C"#column headers and lines (deep blue)
LINE_COLOR  = "#B0B8DC"#row separator lines (light blue)
PRIORITY_LINE = "#E8502A"#vertical separator before Priority col
TEXT_DARK   = "#1a1a2e"#main text color
TEXT_GREY   = "#9a9aaa"#placeholder / greyed-out text
DONE_COLOR  = "#b0b8aa"#color for completed tasks

# ---------------------------------------------------------------
# DATA LOGIC  
# ---------------------------------------------------------------

def load_tasks():
    """Load tasks from the JSON file on disk (Storage -> Memory)."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks):
    """Save the current list of tasks to the JSON file (Memory -> Storage)."""
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task(tasks, task_name, priority="Medium"):
    """Create a new task dictionary and append it to the tasks list."""
    new_task = {
        "id":       len(tasks) + 1,
        "task":     task_name,
        "priority": priority,
        "done":     False
    }
    tasks.append(new_task)
    return tasks


def toggle_task_done(tasks, task_id):
    """Flip the done status of a task."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return True
    return False


def delete_task(tasks, task_id):
    """Remove a task from the list by its id."""
    tasks[:] = [t for t in tasks if t["id"] != task_id]
    return tasks


# ---------------------------------------------------------------
# GUI APPLICATION
# ---------------------------------------------------------------

class TodoApp:
    """
    Main GUI class. Reproduces the visual style of a paper planner
    while connecting every user action to the data logic above.
    """

    def __init__(self, root):
        #--- Window setup ---
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("480x680")
        self.root.configure(bg=BG_CREAM)
        self.root.resizable(False, False)

        #--- Load existing tasks from disk ---
        self.tasks = load_tasks()

        #--- Build all widgets then display tasks ---
        self._build_widgets()
        self._refresh_list()

    # -----------------------------------------------------------
    # WIDGET CONSTRUCTION
    # -----------------------------------------------------------

    def _build_widgets(self):
        """Create every visual element of the planner window."""

        #── TITLE ──────────────────────────────────────────────
        tk.Label(
            self.root,
            text="TO DO LIST",
            font=("Georgia", 26, "bold"),
            bg=BG_CREAM,
            fg=CORAL_RED
        ).pack(pady=(22, 4))

        #thin navy separator under the title
        tk.Frame(self.root, bg=NAVY, height=2).pack(fill="x", padx=24)

        # ── INPUT ROW (task entry + priority + Add button) ─────
        input_frame = tk.Frame(self.root, bg=BG_CREAM)
        input_frame.pack(fill="x", padx=24, pady=(10, 4))

        #task text field
        self.task_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 11),
            bg="#EDEAE0",#slightly darker cream for the field
            fg=TEXT_DARK,
            relief="flat",
            insertbackground=TEXT_DARK
        )
        self.task_entry.pack(side="left", fill="x", expand=True, ipady=5)
        #pressing Enter triggers the same action as clicking Add
        self.task_entry.bind("<Return>", lambda e: self._on_add_task())

        #priority dropdown (High / Medium / Low)
        self.priority_var = tk.StringVar(value="Medium")
        priority_menu = tk.OptionMenu(
            input_frame,
            self.priority_var,
            "High", "Medium", "Low"
        )
        priority_menu.config(
            bg=BG_CREAM, fg=NAVY,
            font=("Helvetica", 10),
            relief="flat", borderwidth=0,
            highlightthickness=0
        )
        priority_menu.pack(side="left", padx=(6, 6))

        #Add button
        tk.Button(
            input_frame,
            text="Add",
            font=("Helvetica", 10, "bold"),
            bg=CORAL_RED, fg="white",
            relief="flat", padx=12, pady=4,
            command=self._on_add_task
        ).pack(side="left")

        #── COLUMN HEADERS (To do | Priority) ─────────────────
        header_frame = tk.Frame(self.root, bg=BG_CREAM)
        header_frame.pack(fill="x", padx=24, pady=(6, 0))

        #blue checkbox icon in header
        tk.Label(
            header_frame,
            text="✔",
            font=("Helvetica", 12, "bold"),
            bg=NAVY, fg="white",
            width=2, pady=3
        ).pack(side="left")

        #"To do" header label
        tk.Label(
            header_frame,
            text="  To do",
            font=("Helvetica", 11, "bold"),
            bg=NAVY, fg="white",
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        #vertical coral separator  (1 px wide label tricks)
        tk.Label(
            header_frame,
            text=" Priority ",
            font=("Helvetica", 11, "bold"),
            bg=NAVY, fg="white",
            width=9
        ).pack(side="right")

        #thin navy separator under the header
        tk.Frame(self.root, bg=NAVY, height=1).pack(fill="x", padx=24)

        #── TASK LIST AREA ─────────────────────────────────────
        #We use a Canvas + inner Frame so we can draw custom rows
        #(checkboxes, two columns, coloured lines) that a plain
        #Listbox can't do.
        list_container = tk.Frame(self.root, bg=BG_CREAM)
        list_container.pack(fill="both", expand=True, padx=24)

        self.canvas = tk.Canvas(
            list_container,
            bg=BG_CREAM,
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            list_container,
            orient="vertical",
            command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        #this inner frame lives inside the canvas and holds the rows
        self.list_frame = tk.Frame(self.canvas, bg=BG_CREAM)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.list_frame, anchor="nw"
        )

        #make the canvas resize with its content
        self.list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(
                self.canvas_window, width=e.width
            )
        )

        #── ACTION BUTTONS (Task Done / Delete) ──────────────
        btn_frame = tk.Frame(self.root, bg=BG_CREAM)
        btn_frame.pack(fill="x", padx=24, pady=(6, 4))

        tk.Button(
            btn_frame,
            text="✔  Task Done",
            font=("Helvetica", 10, "bold"),
            bg=NAVY, fg="white",
            relief="flat", pady=6,
            command=self._on_toggle_done
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        tk.Button(
            btn_frame,
            text="🗑  Delete",
            font=("Helvetica", 10, "bold"),
            bg=CORAL_RED, fg="white",
            relief="flat", pady=6,
            command=self._on_delete_task
        ).pack(side="right", expand=True, fill="x", padx=(4, 0))

        #── MEMO SECTION ───────────────────────────────────────
        memo_outer = tk.Frame(
            self.root,
            bg=BG_CREAM,
            highlightbackground=NAVY,
            highlightthickness=1
        )
        memo_outer.pack(fill="x", padx=24, pady=(4, 16))

        tk.Label(
            memo_outer,
            text="Memo",
            font=("Helvetica", 10, "bold"),
            bg=BG_CREAM, fg=CORAL_RED,
            anchor="w"
        ).pack(fill="x", padx=6, pady=(4, 0))

        self.memo_text = tk.Text(
            memo_outer,
            height=3,
            font=("Helvetica", 10),
            bg=BG_CREAM, fg=TEXT_DARK,
            relief="flat",
            insertbackground=TEXT_DARK,
            wrap="word"
        )
        self.memo_text.pack(fill="x", padx=6, pady=(0, 6))

        #── STATUS BAR ─────────────────────────────────────────
        self.status_var = tk.StringVar()
        tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Helvetica", 9),
            bg=BG_CREAM, fg=TEXT_GREY
        ).pack(pady=(0, 6))

        #track which task row is currently selected
        self.selected_id = None

    # -----------------------------------------------------------
    # CALLBACKS
    # -----------------------------------------------------------

    def _on_add_task(self):
        """Called when the user clicks Add or presses Enter."""
        task_name = self.task_entry.get().strip()
        if not task_name:
            messagebox.showwarning("Empty task", "Please type a task first.")
            return

        priority = self.priority_var.get()
        self.tasks = add_task(self.tasks, task_name, priority)
        save_tasks(self.tasks)
        self.task_entry.delete(0, tk.END)
        self._refresh_list()

    def _on_toggle_done(self):
        """Mark the selected task as done / not done."""
        if self.selected_id is None:
            messagebox.showinfo("No selection", "Please click a task first.")
            return
        toggle_task_done(self.tasks, self.selected_id)
        save_tasks(self.tasks)
        self._refresh_list()

    def _on_delete_task(self):
        """Delete the selected task."""
        if self.selected_id is None:
            messagebox.showinfo("No selection", "Please click a task first.")
            return
        self.tasks = delete_task(self.tasks, self.selected_id)
        self.selected_id = None
        save_tasks(self.tasks)
        self._refresh_list()

    def _select_task(self, task_id, row_frame):
        """Highlight the clicked row and remember its id."""
        self.selected_id = task_id
        #reset all rows to cream, then highlight the chosen one
        for child in self.list_frame.winfo_children():
            child.configure(bg=BG_CREAM)
            for sub in child.winfo_children():
                try:
                    sub.configure(bg=BG_CREAM)
                except Exception:
                    pass
        row_frame.configure(bg="#E8E2D0")
        for sub in row_frame.winfo_children():
            try:
                sub.configure(bg="#E8E2D0")
            except Exception:
                pass

    # -----------------------------------------------------------
    #REFRESH  (Output step — redraws the whole task list)
    # -----------------------------------------------------------

    def _refresh_list(self):
        """
        Clear every row widget inside list_frame and rebuild them
        from scratch using the current state of self.tasks.
        This is the OUTPUT step of the IPO model.
        """
        #destroy all existing row widgets
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.selected_id = None

        #build one row per task
        for task in self.tasks:
            task_id   = task["id"]
            is_done   = task["done"]
            task_text = task["task"]
            priority  = task.get("priority", "Medium")

            #choose colours based on priority and done state
            priority_colors = {
                "High":   CORAL_RED,
                "Medium": NAVY,
                "Low":    "#4a9a4a"
            }
            prio_color = priority_colors.get(priority, NAVY)
            text_color = DONE_COLOR if is_done else TEXT_DARK
            checkbox   = "✔" if is_done else "○"

            #── one row frame ──
            row = tk.Frame(self.list_frame, bg=BG_CREAM)
            row.pack(fill="x")

            #checkbox label (clickable)
            cb_label = tk.Label(
                row,
                text=checkbox,
                font=("Helvetica", 12),
                bg=BG_CREAM,
                fg=NAVY if not is_done else DONE_COLOR,
                width=2
            )
            cb_label.pack(side="left", padx=(2, 4))

            #task name label (clickable to select the row)
            task_label = tk.Label(
                row,
                text=task_text,
                font=("Helvetica", 11,
                      "overstrike" if is_done else "normal"),
                bg=BG_CREAM,
                fg=text_color,
                anchor="w"
            )
            task_label.pack(side="left", fill="x", expand=True)

            #coral vertical separator before priority
            tk.Frame(row, bg=PRIORITY_LINE, width=2).pack(
                side="left", fill="y", padx=(4, 4)
            )

            #priority label
            tk.Label(
                row,
                text=priority,
                font=("Helvetica", 10, "bold"),
                bg=BG_CREAM,
                fg=prio_color,
                width=8
            ).pack(side="right", padx=(0, 4))

            #bind click on every part of the row to _select_task
            for widget in (row, cb_label, task_label):
                widget.bind(
                    "<Button-1>",
                    lambda e, tid=task_id, r=row: self._select_task(tid, r)
                )

            #thin blue separator line under each row
            tk.Frame(self.list_frame, bg=LINE_COLOR, height=1).pack(
                fill="x"
            )

        #update status bar
        total = len(self.tasks)
        done  = sum(1 for t in self.tasks if t["done"])
        self.status_var.set(f"{done} of {total} tasks completed")


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------

def main():
    root = tk.Tk()
    app  = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()