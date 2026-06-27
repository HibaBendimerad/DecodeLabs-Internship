"""
Project 2: Expense Tracker (GUI Version - Budget Planner Design)
DecodeLabs Industrial Training Kit - Python Programming

Same data logic as the CLI version.
Visual style inspired by a classic Budget Planner:
- Cream/ivory background
- Navy blue serif titles (Georgia font)
- Pastel category colors
- Clean table layout with thin lines
- Overview section with totals
- Monthly Reflections memo section
"""

import json
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "expenses.json"

# ---------------------------------------------------------------
# COLOUR PALETTE  (Budget Planner — pastel & navy)
# ---------------------------------------------------------------
BG_CREAM     = "#F5F0E8"   # ivory/cream background
BG_SECTION   = "#EDE8DF"   # slightly darker for section headers
NAVY         = "#1B3A6B"   # deep navy blue (titles & headers)
LINE_COLOR   = "#C8C0B0"   # warm grey lines (table separators)
TEXT_DARK    = "#2C2C2C"   # near-black for content
TEXT_GREY    = "#9A9080"   # muted grey for labels
HEADER_BG    = "#E8E0D0"   # warm beige for column headers
SELECT_BG    = "#DDD5C5"   # selected row highlight

# Pastel category colours (soft, not aggressive)
CATEGORY_COLORS = {
    "Food":      "#C0785A",   # terracotta pastel
    "Transport": "#4A7FA5",   # steel blue pastel
    "Shopping":  "#7A6EA0",   # lavender pastel
    "Health":    "#4A8C6A",   # sage green pastel
    "Other":     "#A08040",   # warm mustard pastel
}
CATEGORIES = list(CATEGORY_COLORS.keys())

# Pastel bar chart fills (lighter version of category colors)
BAR_PASTELS = {
    "Food":      "#E8B09A",
    "Transport": "#A0C4DC",
    "Shopping":  "#C0B8DC",
    "Health":    "#98CCA8",
    "Other":     "#D4B870",
}


# ---------------------------------------------------------------
# DATA LOGIC  (unchanged)
# ---------------------------------------------------------------

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)


def compute_total(expenses):
    return round(sum(e["amount"] for e in expenses), 2)


def compute_by_category(expenses):
    totals = {}
    for e in expenses:
        cat = e["category"]
        totals[cat] = round(totals.get(cat, 0) + e["amount"], 2)
    return totals


def delete_expense(expenses, expense_id):
    expenses[:] = [e for e in expenses if e["id"] != expense_id]
    return expenses


# ---------------------------------------------------------------
# GUI APPLICATION
# ---------------------------------------------------------------

class ExpenseApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Budget Planner — Expense Tracker")
        self.root.geometry("520x750")
        self.root.configure(bg=BG_CREAM)
        self.root.resizable(False, False)

        self.expenses    = load_expenses()
        self.selected_id = None

        self._build_widgets()
        self._refresh()

        # KILL SWITCH: intercept window close button
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # -----------------------------------------------------------
    # KILL SWITCH — Graceful Shutdown
    # -----------------------------------------------------------

    def _on_close(self):
        """
        Triggered when the user clicks the X button.
        Displays the final session summary before closing —
        the GUI equivalent of the CLI sentinel value 'done'.
        """
        total = compute_total(self.expenses)
        n     = len(self.expenses)
        messagebox.showinfo(
            "Session Summary",
            f"Session closed.\n\n"
            f"Expenses recorded : {n}\n"
            f"─────────────────────\n"
            f"TOTAL SPENT       : ${total:.2f}"
        )
        self.root.destroy()

    # -----------------------------------------------------------
    # HELPER — section title label (matches Budget Planner style)
    # -----------------------------------------------------------

    def _section_title(self, parent, text):
        """Navy spaced-letter section heading like the image."""
        tk.Label(
            parent, text=text,
            font=("Georgia", 10, "bold"),
            bg=BG_CREAM, fg=NAVY,
            anchor="w"
        ).pack(fill="x", padx=24, pady=(10, 2))
        tk.Frame(parent, bg=NAVY, height=1).pack(fill="x", padx=24)

    # -----------------------------------------------------------
    # WIDGET CONSTRUCTION
    # -----------------------------------------------------------

    def _build_widgets(self):

        # ── MAIN TITLE ─────────────────────────────────────────
        title_frame = tk.Frame(self.root, bg=BG_CREAM)
        title_frame.pack(fill="x", padx=24, pady=(20, 0))

        tk.Label(
            title_frame,
            text="BUDGET PLANNER",
            font=("Georgia", 24, "bold"),
            bg=BG_CREAM, fg=NAVY
        ).pack(side="left")

        # subtitle on the right
        tk.Label(
            title_frame,
            text="Expense Tracker",
            font=("Georgia", 10, "italic"),
            bg=BG_CREAM, fg=TEXT_GREY
        ).pack(side="right", anchor="s", pady=(0, 4))

        # thick navy separator under title
        tk.Frame(self.root, bg=NAVY, height=2).pack(
            fill="x", padx=24, pady=(4, 0))

        # ── ADD EXPENSE SECTION ────────────────────────────────
        self._section_title(self.root, "NEW ENTRY")

        input_outer = tk.Frame(
            self.root, bg=HEADER_BG,
            highlightbackground=LINE_COLOR,
            highlightthickness=1
        )
        input_outer.pack(fill="x", padx=24, pady=(4, 0))

        # row 1 : amount + category + add button
        row1 = tk.Frame(input_outer, bg=HEADER_BG)
        row1.pack(fill="x", padx=8, pady=(8, 4))

        tk.Label(row1, text="AMOUNT",
                 font=("Georgia", 8), bg=HEADER_BG,
                 fg=TEXT_GREY).pack(side="left")

        tk.Label(row1, text="$",
                 font=("Georgia", 12, "bold"),
                 bg=HEADER_BG, fg=NAVY).pack(side="left", padx=(4, 0))

        self.amount_entry = tk.Entry(
            row1, font=("Georgia", 11),
            bg=BG_CREAM, fg=TEXT_DARK,
            relief="flat", insertbackground=NAVY, width=9,
            highlightthickness=1,
            highlightbackground=LINE_COLOR
        )
        self.amount_entry.pack(side="left", ipady=4, padx=(2, 12))

        tk.Label(row1, text="CATEGORY",
                 font=("Georgia", 8), bg=HEADER_BG,
                 fg=TEXT_GREY).pack(side="left")

        self.category_var = tk.StringVar(value="Food")
        cat_menu = tk.OptionMenu(row1, self.category_var, *CATEGORIES)
        cat_menu.config(
            bg=BG_CREAM, fg=NAVY,
            font=("Georgia", 10),
            relief="flat", borderwidth=1,
            highlightthickness=1,
            highlightbackground=LINE_COLOR,
            activebackground=SELECT_BG
        )
        cat_menu.pack(side="left", padx=(4, 12))

        tk.Button(
            row1, text="ADD ENTRY",
            font=("Georgia", 9, "bold"),
            bg=NAVY, fg=BG_CREAM,
            relief="flat", padx=12, pady=4,
            activebackground="#2A5298",
            command=self._on_add
        ).pack(side="left")

        # row 2 : description
        row2 = tk.Frame(input_outer, bg=HEADER_BG)
        row2.pack(fill="x", padx=8, pady=(0, 8))

        tk.Label(row2, text="DESCRIPTION / NOTES",
                 font=("Georgia", 8),
                 bg=HEADER_BG, fg=TEXT_GREY).pack(side="left")

        self.desc_entry = tk.Entry(
            row2, font=("Georgia", 10),
            bg=BG_CREAM, fg=TEXT_DARK,
            relief="flat", insertbackground=NAVY,
            highlightthickness=1,
            highlightbackground=LINE_COLOR
        )
        self.desc_entry.pack(
            side="left", fill="x", expand=True,
            ipady=4, padx=(8, 0))

        self.amount_entry.bind("<Return>", lambda e: self._on_add())
        self.desc_entry.bind("<Return>",   lambda e: self._on_add())

        # ── FIXED EXPENSES TABLE ───────────────────────────────
        self._section_title(self.root, "EXPENSES")

        # column headers (like the image)
        hdr_frame = tk.Frame(
            self.root, bg=HEADER_BG,
            highlightbackground=LINE_COLOR,
            highlightthickness=1
        )
        hdr_frame.pack(fill="x", padx=24)

        col_specs = [
            ("#",           3,  "center"),
            ("CATEGORY",    10, "w"),
            ("AMOUNT",      9,  "e"),
            ("DETAILS/NOTES", 20, "w"),
        ]
        for text, w, anchor in col_specs:
            tk.Label(
                hdr_frame, text=text,
                font=("Georgia", 8, "bold"),
                bg=HEADER_BG, fg=NAVY,
                width=w, anchor=anchor,
                pady=4
            ).pack(side="left", padx=2)

        # scrollable list area
        list_container = tk.Frame(
            self.root, bg=BG_CREAM,
            highlightbackground=LINE_COLOR,
            highlightthickness=1
        )
        list_container.pack(
            fill="both", expand=True, padx=24)

        self.canvas = tk.Canvas(
            list_container, bg=BG_CREAM,
            highlightthickness=0, height=175)
        sb = tk.Scrollbar(
            list_container, orient="vertical",
            command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.list_frame = tk.Frame(self.canvas, bg=BG_CREAM)
        self._cw = self.canvas.create_window(
            (0, 0), window=self.list_frame, anchor="nw")

        self.list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")))
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(
                self._cw, width=e.width))

        # action buttons row
        btn_frame = tk.Frame(self.root, bg=BG_CREAM)
        btn_frame.pack(fill="x", padx=24, pady=(4, 0))

        tk.Button(
            btn_frame, text="DELETE SELECTED",
            font=("Georgia", 8, "bold"),
            bg=BG_SECTION, fg=NAVY,
            relief="flat", pady=4,
            highlightthickness=1,
            highlightbackground=LINE_COLOR,
            command=self._on_delete
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        tk.Button(
            btn_frame, text="RESET ALL",
            font=("Georgia", 8, "bold"),
            bg=BG_SECTION, fg=NAVY,
            relief="flat", pady=4,
            highlightthickness=1,
            highlightbackground=LINE_COLOR,
            command=self._on_reset
        ).pack(side="right", expand=True, fill="x", padx=(4, 0))

        # ── OVERVIEW SECTION  (inspired by image) ──────────────
        self._section_title(self.root, "OVERVIEW")

        overview_frame = tk.Frame(
            self.root, bg=BG_CREAM,
            highlightbackground=LINE_COLOR,
            highlightthickness=1
        )
        overview_frame.pack(fill="x", padx=24)

        for label_text, var_name, color in [
            ("TOTAL EXPENSE", "total_label",   NAVY),
            ("BY CATEGORY",   "cat_label",     TEXT_GREY),
        ]:
            row = tk.Frame(overview_frame, bg=BG_CREAM)
            row.pack(fill="x")

            tk.Label(
                row, text=label_text,
                font=("Georgia", 8, "bold"),
                bg=HEADER_BG, fg=NAVY,
                width=16, anchor="w", pady=3, padx=4
            ).pack(side="left")

            tk.Frame(row, bg=LINE_COLOR, width=1).pack(
                side="left", fill="y")

            lbl = tk.Label(
                row, text="—",
                font=("Georgia", 9),
                bg=BG_CREAM, fg=color,
                anchor="w", padx=8
            )
            lbl.pack(side="left", fill="x", expand=True)
            setattr(self, var_name, lbl)

            tk.Frame(overview_frame, bg=LINE_COLOR, height=1
                     ).pack(fill="x")

        # ── BAR CHART ──────────────────────────────────────────
        self._section_title(self.root, "SPENDING BY CATEGORY")

        self.chart_canvas = tk.Canvas(
            self.root, bg=BG_CREAM,
            highlightthickness=1,
            highlightbackground=LINE_COLOR,
            height=85)
        self.chart_canvas.pack(fill="x", padx=24, pady=(0, 4))

        # ── MONTHLY REFLECTIONS  (memo from image) ─────────────
        self._section_title(self.root, "MONTHLY REFLECTIONS")

        memo_frame = tk.Frame(
            self.root, bg=BG_CREAM,
            highlightbackground=LINE_COLOR,
            highlightthickness=1
        )
        memo_frame.pack(fill="x", padx=24, pady=(0, 4))

        self.memo_text = tk.Text(
            memo_frame, height=3,
            font=("Georgia", 9),
            bg=BG_CREAM, fg=TEXT_DARK,
            relief="flat",
            insertbackground=NAVY,
            wrap="word"
        )
        self.memo_text.pack(fill="x", padx=6, pady=6)

        # ── STATUS BAR ─────────────────────────────────────────
        self.status_var = tk.StringVar()
        tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Georgia", 8, "italic"),
            bg=BG_CREAM, fg=TEXT_GREY
        ).pack(pady=(0, 6))

    # -----------------------------------------------------------
    # CALLBACKS
    # -----------------------------------------------------------

    def _on_add(self):
        raw = self.amount_entry.get().strip()
        try:
            amount = float(raw)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid Amount",
                "Please enter a positive number (e.g. 12.50).")
            return

        category    = self.category_var.get()
        description = self.desc_entry.get().strip() or "—"

        self.expenses = load_expenses()
        self.expenses.append({
            "id":          len(self.expenses) + 1,
            "amount":      round(amount, 2),
            "category":    category,
            "description": description
        })
        save_expenses(self.expenses)

        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self._refresh()

    def _on_delete(self):
        if self.selected_id is None:
            messagebox.showinfo(
                "No Selection",
                "Please click an expense row first.")
            return
        self.expenses = delete_expense(self.expenses, self.selected_id)
        self.selected_id = None
        save_expenses(self.expenses)
        self._refresh()

    def _on_reset(self):
        if not self.expenses:
            return
        if messagebox.askyesno("Reset All", "Delete ALL expenses?"):
            self.expenses    = []
            self.selected_id = None
            save_expenses(self.expenses)
            self._refresh()

    def _select_row(self, expense_id, row_frame):
        """Highlight the clicked row and remember its id."""
        self.selected_id = expense_id
        for child in self.list_frame.winfo_children():
            child.configure(bg=BG_CREAM)
            for sub in list(child.winfo_children()):
                try:
                    sub.configure(bg=BG_CREAM)
                except Exception:
                    pass
        row_frame.configure(bg=SELECT_BG)
        for sub in list(row_frame.winfo_children()):
            try:
                sub.configure(bg=SELECT_BG)
            except Exception:
                pass

    # -----------------------------------------------------------
    # REFRESH  (Output step)
    # -----------------------------------------------------------

    def _refresh(self):
        """Redraw everything from current self.expenses state."""

        # clear existing rows
        for w in self.list_frame.winfo_children():
            w.destroy()
        self.selected_id = None

        # build one row per expense
        for e in self.expenses:
            color  = CATEGORY_COLORS.get(e["category"], NAVY)
            row    = tk.Frame(self.list_frame, bg=BG_CREAM)
            row.pack(fill="x")

            # ID
            tk.Label(
                row, text=f"{e['id']:>2}",
                font=("Georgia", 9),
                bg=BG_CREAM, fg=TEXT_GREY,
                width=3, anchor="center"
            ).pack(side="left", padx=(4, 0))

            # category (colored)
            tk.Label(
                row, text=e["category"],
                font=("Georgia", 9, "bold"),
                bg=BG_CREAM, fg=color,
                width=10, anchor="w"
            ).pack(side="left")

            # amount (monospaced for alignment)
            tk.Label(
                row, text=f"${e['amount']:>8.2f}",
                font=("Courier", 9, "bold"),
                bg=BG_CREAM, fg=TEXT_DARK,
                width=10, anchor="e"
            ).pack(side="left")

            # thin separator
            tk.Frame(row, bg=LINE_COLOR, width=1).pack(
                side="left", fill="y", padx=4)

            # description
            tk.Label(
                row, text=e["description"],
                font=("Georgia", 9),
                bg=BG_CREAM, fg=TEXT_DARK,
                anchor="w"
            ).pack(side="left", fill="x", expand=True)

            # bind click on the whole row
            for widget in (row,) + tuple(row.winfo_children()):
                widget.bind(
                    "<Button-1>",
                    lambda ev, eid=e["id"], r=row:
                        self._select_row(eid, r))

            # thin line separator
            tk.Frame(self.list_frame, bg=LINE_COLOR, height=1
                     ).pack(fill="x")

        # update overview labels
        total = compute_total(self.expenses)
        self.total_label.configure(text=f"  ${total:.2f}")

        by_cat  = compute_by_category(self.expenses)
        cat_str = "  " + "   ".join(
            f"{c}: ${v:.0f}" for c, v in by_cat.items()
        ) if by_cat else "  —"
        self.cat_label.configure(text=cat_str)

        # update status
        n = len(self.expenses)
        self.status_var.set(
            f"{n} entr{'ies' if n != 1 else 'y'} recorded")

        self._draw_chart()

    def _draw_chart(self):
        """Horizontal bar chart with pastel fills."""
        self.chart_canvas.delete("all")
        by_cat = compute_by_category(self.expenses)

        if not by_cat:
            self.chart_canvas.create_text(
                240, 42,
                text="No expenses yet — add your first entry above",
                fill=TEXT_GREY, font=("Georgia", 9, "italic"))
            return

        total    = compute_total(self.expenses)
        bar_area = 290
        x_start  = 85
        row_h    = 16
        y_start  = 6

        for i, (cat, amount) in enumerate(by_cat.items()):
            y      = y_start + i * row_h
            color  = CATEGORY_COLORS.get(cat, NAVY)
            pastel = BAR_PASTELS.get(cat, "#B0C0D0")
            bar_w  = int((amount / total) * bar_area) if total else 0

            # label
            self.chart_canvas.create_text(
                x_start - 6, y + 7,
                text=cat.upper(),
                anchor="e",
                fill=NAVY,
                font=("Georgia", 7, "bold"))

            # background track
            self.chart_canvas.create_rectangle(
                x_start, y + 2,
                x_start + bar_area, y + 13,
                fill="#E8E0D0", outline=LINE_COLOR)

            # filled bar (pastel)
            if bar_w > 0:
                self.chart_canvas.create_rectangle(
                    x_start, y + 2,
                    x_start + bar_w, y + 13,
                    fill=pastel, outline="")

            # amount
            self.chart_canvas.create_text(
                x_start + bar_area + 6, y + 7,
                text=f"${amount:.2f}",
                anchor="w",
                fill=color,
                font=("Georgia", 7, "bold"))


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------

def main():
    root = tk.Tk()
    ExpenseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()