# 💸 Task 2 — Expense Tracker

> **DecodeLabs Python Programming Internship | Batch 2026**
> Project 2 of the Industrial Training Kit

---

##  Project Goal

Build a program where users enter expense amounts and categories.
The program accumulates them in real-time and displays the **Total Spent**,
broken down by category — the foundational logic behind every financial
application ever built.

---

##  Features

| Feature | CLI | GUI |
|---------|:---:|:---:|
| Add expense with amount + category | ✅ | ✅ |
| Add optional description | ✅ | ✅ |
| Real-time running total (accumulator) | ✅ | ✅ |
| Breakdown by category | ✅ | ✅ |
| Live bar chart by category | — | ✅ |
| Delete a specific expense | ✅ | ✅ |
| Reset all expenses | ✅ | ✅ |
| Input validation (try/except) | ✅ | ✅ |
| Persistent storage (JSON) | ✅ | ✅ |

---

##  Concepts Applied

| Concept | Where it appears |
|---------|-----------------|
| **Accumulator pattern** | `total += amount` — running total updated on every entry |
| **Type conversion** | `float(input())` — converts raw string to decimal number |
| **try / except ValueError** | Catches invalid input (e.g. "bonjour") without crashing |
| **Sentinel / Kill Switch** | Option 4 in CLI triggers graceful shutdown with final total |
| **Dictionaries** | Each expense stored as `{"id", "amount", "category", "description"}` |
| **JSON persistence** | `expenses.json` saves data between sessions |
| **`sum()` + generator** | `sum(e["amount"] for e in expenses)` — Pythonic accumulation |
| **Canvas widget** | Live bar chart drawn programmatically in Tkinter |
| **IPO model** | Input → Process (accumulate) → Output (chart + total) |

---

##  Architecture

```
INPUT                   PROCESS                  OUTPUT
─────                   ───────                  ──────
User enters      →    float() converts     →   Total label updates
amount + cat           try/except guards        Bar chart redraws
                        add_expense() stores     expenses.json saved
                        compute_total() sums
```

The accumulator in plain Python:
```python
total = 0                        # initialized ONCE, BEFORE the loop
for expense in expenses:
    total += expense["amount"]   # += adds to the running total
```

Equivalent Pythonic shorthand used in the code:
```python
total = sum(e["amount"] for e in expenses)
```

---

##  How to Run

### Command-line version
```bash
python3 expense_tracker.py
```

### Graphical version (GUI)
```bash
python3 expense_tracker_gui.py
```

> **Linux users:** if Tkinter is missing: `sudo apt install python3-tk`

---

##  File Structure

```
Task-2-Expense-Tracker/
├── expense_tracker.py       # Command-line version
├── expense_tracker_gui.py   # Graphical version with live bar chart
├── expenses.json            # Auto-generated — do NOT delete
└── README.md                # This file
```

---

*Built with Python 3 | DecodeLabs Internship Batch 2026*