"""
Project 4: General Knowledge Quiz (CLI Version)
DecodeLabs Industrial Training Kit - Python Programming

This program runs a general knowledge quiz.
It applies the IPOS model:
- Input    : user answers (sanitized with .strip().lower())
- Process  : if/elif/else control flow evaluates correctness
- Output   : per-question feedback + final score + grade
- Storage  : quiz history saved to JSON

Key concepts: control flow (if/elif/else), input sanitization,
              functions with return values, score accumulator,
              list operations, f-strings, JSON persistence.
"""

import json
import os
from datetime import datetime

HISTORY_FILE = "quiz_history.json"

# ---------------------------------------------------------------
# QUIZ DATA — list of question dictionaries
# Each question has: text, list of accepted answers, hint, category
# ---------------------------------------------------------------
QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "answers":  ["paris"],
        "hint":     "City of Light 🗼",
        "category": "Geography"
    },
    {
        "question": "How many planets are in our solar system?",
        "answers":  ["8", "eight"],
        "hint":     "Pluto was reclassified in 2006",
        "category": "Science"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "answers":  ["leonardo da vinci", "da vinci", "leonardo"],
        "hint":     "Italian Renaissance master 🎨",
        "category": "Art"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "answers":  ["pacific", "pacific ocean"],
        "hint":     "Covers more than 30% of Earth's surface",
        "category": "Geography"
    },
    {
        "question": "In what year did World War II end?",
        "answers":  ["1945"],
        "hint":     "Allied victory in Europe was in May of that year",
        "category": "History"
    },
    {
        "question": "What programming language are you using right now?",
        "answers":  ["python"],
        "hint":     "Named after a British comedy group 🐍",
        "category": "Technology"
    },
    {
        "question": "What is the chemical symbol for water?",
        "answers":  ["h2o"],
        "hint":     "Two hydrogens, one oxygen",
        "category": "Science"
    },
    {
        "question": "How many sides does a hexagon have?",
        "answers":  ["6", "six"],
        "hint":     "Think of a honeycomb cell 🍯",
        "category": "Mathematics"
    },
    {
        "question": "What is the fastest land animal?",
        "answers":  ["cheetah"],
        "hint":     "Can reach 110 km/h in short bursts",
        "category": "Nature"
    },
    {
        "question": "Who wrote Romeo and Juliet?",
        "answers":  ["shakespeare", "william shakespeare"],
        "hint":     "The Bard of Avon ✍️",
        "category": "Literature"
    },
]


# ---------------------------------------------------------------
# DATA LOGIC
# ---------------------------------------------------------------

def load_history():
    """Load quiz history from disk."""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_history(history):
    """Save quiz history to disk."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def sanitize_input(raw):
    """
    Input sanitization pipeline: strip whitespace then lowercase.
    THE PRO RECIPE: .strip().lower()
    - .strip()  → removes accidental leading/trailing spaces
    - .lower()  → neutralizes case sensitivity ('Paris' == 'paris')
    Always strip BEFORE lower — order matters.
    """
    return raw.strip().lower()


def is_correct(user_answer, accepted_answers):
    """
    Control flow gate: check sanitized answer against all accepted answers.
    Returns True if any accepted answer matches.
    """
    clean = sanitize_input(user_answer)
    return clean in accepted_answers


def get_grade_letter(score, total):
    """
    Convert a score to a letter grade using if/elif/else control flow.
    The percentage determines which branch executes.
    """
    if total == 0:
        return "N/A"

    pct = (score / total) * 100

    if pct >= 90:
        return "A ⭐"
    elif pct >= 80:
        return "B 👍"
    elif pct >= 70:
        return "C 🙂"
    elif pct >= 60:
        return "D 😐"
    else:
        return "F 📚"


def get_performance_message(score, total):
    """Return a contextual message based on the score."""
    pct = (score / total) * 100 if total else 0
    if pct == 100:
        return "Perfect score! Outstanding performance! 🏆"
    elif pct >= 80:
        return "Great job! You really know your stuff! 🌟"
    elif pct >= 60:
        return "Good effort! Keep studying and you'll ace it! 💪"
    else:
        return "Don't give up! Every mistake is a learning opportunity. 📖"


def ask_question(q_num, total, question_data):
    """
    The Question Block Micro-Architecture (from the PDF):
    Step 1: Ask & Capture  → input()
    Step 2: Sanitize       → .strip().lower()
    Step 3: Evaluate       → if/elif/else
    Step 4: Execute        → increment score, print feedback
    Returns True if correct, False otherwise.
    """
    print(f"\n  ─── Question {q_num}/{total} [{question_data['category']}] ───")
    print(f"  {question_data['question']}")

    user_answer = input("  Your answer: ")

    #Step 2: Sanitize
    #Step 3 & 4: Evaluate and route
    if is_correct(user_answer, question_data["answers"]):
        print("  ✅ Correct!")
        return True
    else:
        hint_text = question_data["hint"]
        correct   = question_data["answers"][0].title()
        print(f"  ❌ Wrong! The answer was: {correct}")
        print(f"  💡 Hint was: {hint_text}")
        return False


# ---------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------

def run_quiz(questions):
    """
    Run a quiz session and return the results dictionary.
    The score accumulator starts at 0 and increments on correct answers.
    """
    print("\n" + "═" * 50)
    print("   🧠 GENERAL KNOWLEDGE QUIZ")
    print("═" * 50)
    print(f"  {len(questions)} questions | Type your answer and press Enter")
    print("═" * 50)

    #STORAGE: score = 0 — The Score Vault (accumulator)
    score    = 0
    results  = []

    for i, q in enumerate(questions, 1):
        correct = ask_question(i, len(questions), q)

        #PROCESS: if correct → increment score vault
        if correct:
            score += 1

        results.append({
            "question": q["question"],
            "correct":  correct,
            "answer":   q["answers"][0]
        })

    return score, results


def show_final_report(score, total, results):
    """OUTPUT: display the final score summary with grade."""
    pct   = round((score / total) * 100, 1) if total else 0
    grade = get_grade_letter(score, total)
    msg   = get_performance_message(score, total)

    print("\n" + "═" * 50)
    print("   📊 FINAL REPORT")
    print("═" * 50)
    print(f"  Score  : {score} / {total}")
    print(f"  Grade  : {grade}")
    print(f"  Result : {pct}%")
    print(f"\n  {msg}")
    print("═" * 50)

    #Breakdown
    print("\n  Question breakdown:")
    for i, r in enumerate(results, 1):
        icon = "✅" if r["correct"] else "❌"
        print(f"  {icon} Q{i}: {r['question'][:45]}...")

    print()


def show_menu():
    print("\n=== QUIZ APP ===")
    print("1. Start Quiz (10 questions)")
    print("2. Quick Quiz (5 random questions)")
    print("3. View history")
    print("4. Exit")


def main():
    import random
    history = load_history()

    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            score, results = run_quiz(QUESTIONS)
            show_final_report(score, len(QUESTIONS), results)

            history.append({
                "date":    datetime.now().strftime("%Y-%m-%d %H:%M"),
                "score":   score,
                "total":   len(QUESTIONS),
                "grade":   get_grade_letter(score, len(QUESTIONS)),
                "percent": round((score / len(QUESTIONS)) * 100, 1)
            })
            save_history(history)

        elif choice == "2":
            quick_q = random.sample(QUESTIONS, 5)
            score, results = run_quiz(quick_q)
            show_final_report(score, 5, results)

            history.append({
                "date":    datetime.now().strftime("%Y-%m-%d %H:%M"),
                "score":   score,
                "total":   5,
                "grade":   get_grade_letter(score, 5),
                "percent": round((score / 5) * 100, 1)
            })
            save_history(history)

        elif choice == "3":
            if not history:
                print("\nNo quiz attempts yet.\n")
            else:
                print("\n--- QUIZ HISTORY ---")
                for i, h in enumerate(history, 1):
                    print(f"  {i:>2}. {h['date']}  "
                          f"{h['score']}/{h['total']}  "
                          f"{h['percent']}%  {h['grade']}")
                print()

        elif choice == "4":
            #SENTINEL / KILL SWITCH
            n = len(history)
            print(f"\nGoodbye! You completed {n} quiz session(s). Keep learning! 🧠")
            break

        else:
            print("Invalid option. Please choose between 1 and 4.\n")


if __name__ == "__main__":
    main()