# Task 4 — General Knowledge Quiz

> **DecodeLabs Python Programming Internship | Batch 2026**
> Project 4 — Optional Mastery Phase (Control Flow & Decision Engines)

---

## Project Goal

Build a general knowledge quiz that asks questions, evaluates user answers with **if/elif/else control flow**, tracks a running score, and displays a final grade — demonstrating the full IPOS model in a stateful, interactive application.

---

## Features

| Feature | CLI | GUI |
|---------|:---:|:---:|
| 10-question full quiz | ✅ | ✅ |
| 5-question quick quiz (random) | ✅ | ✅ |
| Multiple-choice options | — | ✅ (4 buttons) |
| Input sanitization `.strip().lower()` | ✅ | ✅ |
| Multiple accepted answers per question | ✅ | ✅ |
| Score accumulator (score += 1) | ✅ | ✅ |
| Letter grade (A/B/C/D/F) via if/elif/else | ✅ | ✅ |
| Per-question feedback + hint | ✅ | ✅ |
| Progress bar | — | ✅ |
| Color-coded answer reveal | — | ✅ |
| Question breakdown | ✅ | ✅ |
| History screen with best score | ✅ | ✅ |
| JSON persistence | ✅ | ✅ |
| Kill switch with session summary | ✅ | ✅ |

---

## Concepts Applied

| Concept | Where it appears |
|---------|-----------------|
| **if / elif / else** | `get_grade_letter()` — grade routing; answer evaluation |
| **Input sanitization** | `sanitize_input()` — `.strip().lower()` pipeline |
| **Score accumulator** | `score = 0` then `score += 1` on correct answers |
| **Functions with return** | `is_correct()`, `get_grade_letter()`, `sanitize_input()` |
| **List operations** | `random.sample()`, `random.shuffle()` for question selection |
| **Dictionaries** | Each question stored as a dict with `question`, `answers`, `category`, `options` |
| **JSON persistence** | Quiz history saved to `quiz_history.json` |
| **IPOS model** | Input → Process (evaluate) → Output (feedback) → Storage (history) |
| **Boolean operators** | `in` operator for multi-answer matching |
| **f-strings** | `f"{score}/{total} ({pct}%)"` — formatted score output |

---

## Architecture — The Question Block Micro-Architecture

Per the DecodeLabs PDF, every question follows this precise 4-step block:

```
Step 1: Ask & Capture    → input() or button click
Step 2: Sanitize         → .strip().lower()
Step 3: Evaluate         → if sanitized_answer in accepted_answers
Step 4: Execute          → score += 1 OR show hint
```

---

## How to Run

```bash
# Command-line version
python3 quiz_app.py

# Graphical version (Game Show style)
python3 quiz_app_gui.py
```

---

## File Structure

```
Task-4-Quiz-App/
├── quiz_app.py          # Command-line version
├── quiz_app_gui.py      # Graphical version (Game Show style)
├── quiz_history.json    # Auto-generated — do NOT commit
└── README.md            # This file
```

---

*Built with Python 3 | DecodeLabs Internship Batch 2026 — Final Project*