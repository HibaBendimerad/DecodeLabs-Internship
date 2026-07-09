"""
Project 4: General Knowledge Quiz (GUI Version - Game Show Style)
DecodeLabs Industrial Training Kit - Python Programming

Same data logic as CLI version.
"""

import json
import os
import random
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

HISTORY_FILE = "quiz_history.json"

# ---------------------------------------------------------------
# GAME SHOW COLOUR PALETTE
# ---------------------------------------------------------------
BG_DARK      = "#1A0A2E"   #deep purple background
BG_PANEL     = "#2D1B4E"   #panel purple
BG_CARD      = "#3D2B5E"   #question card
GOLD         = "#FFD700"   #gold accent (titles, score)
GOLD_LIGHT   = "#FFE866"   #lighter gold (hover)
CORRECT_GRN  = "#00C851"   #bright green (correct)
WRONG_RED    = "#FF4444"   #bright red (wrong)
NEUTRAL_BLUE = "#4A9EFF"   #blue (neutral buttons)
PURPLE_LIGHT = "#9B59B6"   #light purple
TEXT_WHITE   = "#FFFFFF"
TEXT_DIM     = "#9B8EC4"
STAR_GOLD    = "#FFA500"

# Category colors
CAT_COLORS = {
    "Geography":   "#4A9EFF",
    "Science":     "#00C851",
    "Art":         "#FF6B9D",
    "History":     "#FFD700",
    "Technology":  "#00D4FF",
    "Mathematics": "#FF8C00",
    "Nature":      "#7CFC00",
    "Literature":  "#DA70D6",
}

# ---------------------------------------------------------------
# QUIZ DATA
# ---------------------------------------------------------------
QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "answers":  ["paris"],
        "hint":     "City of Light 🗼",
        "category": "Geography",
        "options":  ["London", "Berlin", "Paris", "Madrid"]
    },
    {
        "question": "How many planets are in our solar system?",
        "answers":  ["8", "eight"],
        "hint":     "Pluto was reclassified in 2006",
        "category": "Science",
        "options":  ["7", "8", "9", "10"]
    },
    {
        "question": "Who painted the Mona Lisa?",
        "answers":  ["leonardo da vinci", "da vinci", "leonardo"],
        "hint":     "Italian Renaissance master 🎨",
        "category": "Art",
        "options":  ["Michelangelo", "Raphael", "Leonardo da Vinci", "Botticelli"]
    },
    {
        "question": "What is the largest ocean on Earth?",
        "answers":  ["pacific", "pacific ocean"],
        "hint":     "Covers more than 30% of Earth's surface",
        "category": "Geography",
        "options":  ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"]
    },
    {
        "question": "In what year did World War II end?",
        "answers":  ["1945"],
        "hint":     "Allied victory in Europe was in May",
        "category": "History",
        "options":  ["1943", "1944", "1945", "1946"]
    },
    {
        "question": "What programming language are you using right now?",
        "answers":  ["python"],
        "hint":     "Named after a British comedy group 🐍",
        "category": "Technology",
        "options":  ["Java", "Python", "C++", "JavaScript"]
    },
    {
        "question": "What is the chemical symbol for water?",
        "answers":  ["h2o"],
        "hint":     "Two hydrogens, one oxygen",
        "category": "Science",
        "options":  ["CO2", "H2O", "NaCl", "O2"]
    },
    {
        "question": "How many sides does a hexagon have?",
        "answers":  ["6", "six"],
        "hint":     "Think of a honeycomb cell 🍯",
        "category": "Mathematics",
        "options":  ["5", "6", "7", "8"]
    },
    {
        "question": "What is the fastest land animal?",
        "answers":  ["cheetah"],
        "hint":     "Can reach 110 km/h in short bursts",
        "category": "Nature",
        "options":  ["Lion", "Leopard", "Cheetah", "Greyhound"]
    },
    {
        "question": "Who wrote Romeo and Juliet?",
        "answers":  ["shakespeare", "william shakespeare"],
        "hint":     "The Bard of Avon ✍️",
        "category": "Literature",
        "options":  ["Charles Dickens", "Jane Austen", "William Shakespeare", "Homer"]
    },
]


# ---------------------------------------------------------------
# DATA LOGIC  (identical to CLI)
# ---------------------------------------------------------------

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def sanitize_input(raw):
    """Input sanitization: .strip().lower() pipeline."""
    return raw.strip().lower()


def is_correct(user_answer, accepted_answers):
    return sanitize_input(user_answer) in accepted_answers


def get_grade_letter(score, total):
    if total == 0:
        return "N/A"
    pct = (score / total) * 100
    if pct >= 90:   return "A"
    elif pct >= 80: return "B"
    elif pct >= 70: return "C"
    elif pct >= 60: return "D"
    else:           return "F"


def get_grade_color(grade):
    return {
        "A": CORRECT_GRN,
        "B": "#7CFC00",
        "C": GOLD,
        "D": STAR_GOLD,
        "F": WRONG_RED,
    }.get(grade, TEXT_WHITE)


# ---------------------------------------------------------------
# GUI APPLICATION — GAME SHOW STYLE
# ---------------------------------------------------------------

class QuizApp:

    def __init__(self, root):
        self.root = root
        self.root.title("🧠 General Knowledge Quiz — DecodeLabs")
        self.root.geometry("580x720")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self.history       = load_history()
        self.questions     = []
        self.current_idx   = 0
        self.score         = 0
        self.answered      = False
        self.option_btns   = []
        self.results       = []

        self._build_home_screen()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # -----------------------------------------------------------
    # KILL SWITCH
    # -----------------------------------------------------------

    def _on_close(self):
        n = len(self.history)
        messagebox.showinfo(
            "Thanks for playing!",
            f"See you next time! 🧠\n\n"
            f"Quiz sessions completed: {n}")
        self.root.destroy()

    # -----------------------------------------------------------
    # HELPERS
    # -----------------------------------------------------------

    def _clear(self):
        """Destroy all widgets."""
        for w in self.root.winfo_children():
            w.destroy()

    def _stars(self, score, total):
        """Convert score to star rating string."""
        pct = (score / total) * 100 if total else 0
        if pct == 100: return "⭐⭐⭐"
        elif pct >= 60: return "⭐⭐"
        elif pct > 0:   return "⭐"
        else:           return "☆☆☆"

    # -----------------------------------------------------------
    # HOME SCREEN
    # -----------------------------------------------------------

    def _build_home_screen(self):
        self._clear()

        #decorative top bar
        tk.Frame(self.root, bg=GOLD, height=4).pack(fill="x")

        #title
        tk.Label(
            self.root,
            text="🧠",
            font=("Helvetica", 48),
            bg=BG_DARK, fg=GOLD
        ).pack(pady=(30, 0))

        tk.Label(
            self.root,
            text="GENERAL KNOWLEDGE",
            font=("Helvetica", 22, "bold"),
            bg=BG_DARK, fg=GOLD
        ).pack()

        tk.Label(
            self.root,
            text="Q  U  I  Z",
            font=("Helvetica", 14, "bold"),
            bg=BG_DARK, fg=PURPLE_LIGHT
        ).pack()

        tk.Label(
            self.root,
            text="DecodeLabs Industrial Training Kit — Project 4",
            font=("Helvetica", 9),
            bg=BG_DARK, fg=TEXT_DIM
        ).pack(pady=(4, 30))

        #best score display
        if self.history:
            best = max(self.history, key=lambda h: h["percent"])
            tk.Label(
                self.root,
                text=f"🏆  Best Score: {best['score']}/{best['total']}  ({best['percent']}%)",
                font=("Helvetica", 11, "bold"),
                bg=BG_PANEL, fg=GOLD,
                pady=8, padx=20
            ).pack(pady=(0, 20), ipadx=10)

        #mode buttons
        for text, cmd in [
            ("▶  FULL QUIZ  (10 questions)",   lambda: self._start_quiz("full")),
            ("⚡  QUICK QUIZ  (5 questions)",   lambda: self._start_quiz("quick")),
            ("📋  VIEW HISTORY",                 self._show_history),
        ]:
            btn = tk.Button(
                self.root, text=text,
                font=("Helvetica", 12, "bold"),
                bg=BG_PANEL, fg=TEXT_WHITE,
                relief="flat", pady=14,
                activebackground=PURPLE_LIGHT,
                activeforeground=TEXT_WHITE,
                command=cmd
            )
            btn.pack(fill="x", padx=60, pady=6)

        tk.Frame(self.root, bg=GOLD, height=4).pack(
            fill="x", side="bottom")

    # -----------------------------------------------------------
    # QUIZ SCREEN
    # -----------------------------------------------------------

    def _start_quiz(self, mode):
        if mode == "quick":
            self.questions = random.sample(QUESTIONS, 5)
        else:
            self.questions = QUESTIONS[:]

        self.current_idx = 0
        self.score       = 0
        self.results     = []
        self._build_quiz_screen()
        self._load_question()

    def _build_quiz_screen(self):
        self._clear()

        #top bar with score + progress
        top = tk.Frame(self.root, bg=BG_PANEL)
        top.pack(fill="x")

        tk.Frame(self.root, bg=GOLD, height=2).pack(fill="x")

        self.q_counter = tk.Label(
            top, text="",
            font=("Helvetica", 10, "bold"),
            bg=BG_PANEL, fg=TEXT_DIM
        )
        self.q_counter.pack(side="left", padx=16, pady=8)

        self.score_label = tk.Label(
            top, text="⭐ 0",
            font=("Helvetica", 13, "bold"),
            bg=BG_PANEL, fg=GOLD
        )
        self.score_label.pack(side="right", padx=16, pady=8)

        #progress bar
        prog_bg = tk.Frame(self.root, bg="#3D2B5E", height=8)
        prog_bg.pack(fill="x")
        self.progress_fill = tk.Frame(prog_bg, bg=GOLD, height=8)
        self.progress_fill.place(x=0, y=0, width=0, height=8)

        #category badge
        self.cat_badge = tk.Label(
            self.root, text="",
            font=("Helvetica", 9, "bold"),
            bg=BG_DARK, fg=NEUTRAL_BLUE
        )
        self.cat_badge.pack(pady=(20, 0))

        #question card
        card = tk.Frame(
            self.root, bg=BG_CARD,
            highlightbackground=PURPLE_LIGHT,
            highlightthickness=2
        )
        card.pack(fill="x", padx=24, pady=(8, 0))

        self.q_label = tk.Label(
            card, text="",
            font=("Helvetica", 14, "bold"),
            bg=BG_CARD, fg=TEXT_WHITE,
            wraplength=490, justify="center",
            pady=24
        )
        self.q_label.pack(fill="x", padx=20)

        #feedback label
        self.feedback_label = tk.Label(
            self.root, text="",
            font=("Helvetica", 12, "bold"),
            bg=BG_DARK, fg=CORRECT_GRN
        )
        self.feedback_label.pack(pady=(10, 0))

        #hint label
        self.hint_label = tk.Label(
            self.root, text="",
            font=("Helvetica", 9, "italic"),
            bg=BG_DARK, fg=TEXT_DIM
        )
        self.hint_label.pack()

        #4 option buttons
        self.option_btns = []
        for i in range(4):
            btn = tk.Button(
                self.root, text="",
                font=("Helvetica", 11),
                bg=BG_PANEL, fg=TEXT_WHITE,
                relief="flat", pady=12,
                activebackground=PURPLE_LIGHT,
                activeforeground=TEXT_WHITE,
                command=lambda idx=i: self._on_answer(idx)
            )
            btn.pack(fill="x", padx=40, pady=4)
            self.option_btns.append(btn)

        #next button (hidden until answered)
        self.next_btn = tk.Button(
            self.root, text="NEXT QUESTION  ➜",
            font=("Helvetica", 11, "bold"),
            bg=GOLD, fg=BG_DARK,
            relief="flat", pady=10,
            activebackground=GOLD_LIGHT,
            command=self._next_question,
            state="disabled"
        )
        self.next_btn.pack(fill="x", padx=40, pady=(10, 0))

        tk.Frame(self.root, bg=GOLD, height=4).pack(
            fill="x", side="bottom")

    def _load_question(self):
        """Load current question into the UI."""
        self.answered = False
        q = self.questions[self.current_idx]
        total = len(self.questions)

        #update counter + progress bar
        self.q_counter.configure(
            text=f"Question {self.current_idx + 1} of {total}")
        self.score_label.configure(text=f"⭐ {self.score}")

        #progress bar fill
        pct = self.current_idx / total
        bar_w = int(pct * 580)
        self.progress_fill.place(x=0, y=0, width=bar_w, height=8)

        #category badge
        cat_color = CAT_COLORS.get(q["category"], NEUTRAL_BLUE)
        self.cat_badge.configure(
            text=f"  [ {q['category'].upper()} ]  ",
            fg=cat_color)

        #question text
        self.q_label.configure(text=q["question"])

        #feedback + hint reset
        self.feedback_label.configure(text="")
        self.hint_label.configure(text="")

        #shuffle & load options
        options = q["options"][:]
        random.shuffle(options)
        self._current_options = options

        for i, btn in enumerate(self.option_btns):
            btn.configure(
                text=options[i],
                bg=BG_PANEL, fg=TEXT_WHITE,
                state="normal")

        self.next_btn.configure(
            state="disabled",
            text="NEXT QUESTION  ➜" if self.current_idx < total - 1
                 else "SEE RESULTS  ➜",
            bg=GOLD)

    def _on_answer(self, btn_idx):
        """Called when user clicks an option button."""
        if self.answered:
            return
        self.answered = True

        q           = self.questions[self.current_idx]
        chosen_text = self._current_options[btn_idx]
        correct     = is_correct(chosen_text, q["answers"])

        #color ALL buttons: green for correct answer, red for wrong choice
        for i, btn in enumerate(self.option_btns):
            opt = self._current_options[i]
            if is_correct(opt, q["answers"]):
                btn.configure(bg=CORRECT_GRN, fg=BG_DARK)
            elif i == btn_idx and not correct:
                btn.configure(bg=WRONG_RED, fg=TEXT_WHITE)
            else:
                btn.configure(bg=BG_PANEL, fg=TEXT_DIM, state="disabled")
            btn.configure(state="disabled")

        if correct:
            self.score += 1
            self.score_label.configure(text=f"⭐ {self.score}", fg=CORRECT_GRN)
            self.feedback_label.configure(
                text="✅  Correct! Well done!", fg=CORRECT_GRN)
        else:
            correct_ans = q["answers"][0].title()
            self.feedback_label.configure(
                text=f"❌  Wrong! Answer: {correct_ans}", fg=WRONG_RED)
            self.hint_label.configure(
                text=f"💡 {q['hint']}", fg=TEXT_DIM)

        self.results.append({
            "question": q["question"],
            "correct":  correct,
            "answer":   q["answers"][0]
        })

        self.next_btn.configure(state="normal")

    def _next_question(self):
        self.current_idx += 1
        if self.current_idx >= len(self.questions):
            self._show_results()
        else:
            #reset score label color
            self.score_label.configure(fg=GOLD)
            self._load_question()

    # -----------------------------------------------------------
    # RESULTS SCREEN
    # -----------------------------------------------------------

    def _show_results(self):
        self._clear()

        total  = len(self.questions)
        pct    = round((self.score / total) * 100, 1)
        grade  = get_grade_letter(self.score, total)
        gcolor = get_grade_color(grade)
        stars  = self._stars(self.score, total)

        tk.Frame(self.root, bg=GOLD, height=4).pack(fill="x")

        tk.Label(
            self.root, text=stars,
            font=("Helvetica", 36),
            bg=BG_DARK
        ).pack(pady=(24, 0))

        tk.Label(
            self.root, text="QUIZ COMPLETE!",
            font=("Helvetica", 20, "bold"),
            bg=BG_DARK, fg=GOLD
        ).pack()

        #big score display
        score_frame = tk.Frame(
            self.root, bg=BG_PANEL,
            highlightbackground=gcolor,
            highlightthickness=2
        )
        score_frame.pack(padx=60, pady=16, fill="x")

        tk.Label(
            score_frame,
            text=f"{self.score} / {total}",
            font=("Helvetica", 36, "bold"),
            bg=BG_PANEL, fg=gcolor,
            pady=10
        ).pack()

        tk.Label(
            score_frame,
            text=f"Grade: {grade}   |   {pct}%",
            font=("Helvetica", 14),
            bg=BG_PANEL, fg=TEXT_WHITE,
            pady=4
        ).pack()

        #question breakdown (scrollable)
        tk.Label(
            self.root, text="Question Breakdown",
            font=("Helvetica", 10, "bold"),
            bg=BG_DARK, fg=TEXT_DIM
        ).pack(pady=(8, 4))

        breakdown_frame = tk.Frame(self.root, bg=BG_DARK)
        breakdown_frame.pack(fill="x", padx=24)

        for i, r in enumerate(self.results, 1):
            icon  = "✅" if r["correct"] else "❌"
            color = CORRECT_GRN if r["correct"] else WRONG_RED
            row   = tk.Frame(breakdown_frame, bg=BG_DARK)
            row.pack(fill="x", pady=1)
            tk.Label(
                row, text=f"{icon}  Q{i}: {r['question'][:42]}...",
                font=("Helvetica", 9),
                bg=BG_DARK, fg=color, anchor="w"
            ).pack(side="left")

        #save history
        self.history.append({
            "date":    datetime.now().strftime("%Y-%m-%d %H:%M"),
            "score":   self.score,
            "total":   total,
            "grade":   grade,
            "percent": pct
        })
        save_history(self.history)

        #action buttons
        btn_frame = tk.Frame(self.root, bg=BG_DARK)
        btn_frame.pack(fill="x", padx=40, pady=(16, 0))

        tk.Button(
            btn_frame, text="🔄  PLAY AGAIN",
            font=("Helvetica", 11, "bold"),
            bg=CORRECT_GRN, fg=BG_DARK,
            relief="flat", pady=10,
            command=lambda: self._start_quiz(
                "full" if total == 10 else "quick")
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        tk.Button(
            btn_frame, text="🏠  HOME",
            font=("Helvetica", 11, "bold"),
            bg=BG_PANEL, fg=TEXT_WHITE,
            relief="flat", pady=10,
            command=self._build_home_screen
        ).pack(side="right", expand=True, fill="x", padx=(6, 0))

        tk.Frame(self.root, bg=GOLD, height=4).pack(
            fill="x", side="bottom")

    # -----------------------------------------------------------
    # HISTORY SCREEN
    # -----------------------------------------------------------

    def _show_history(self):
        self._clear()

        tk.Frame(self.root, bg=GOLD, height=4).pack(fill="x")

        tk.Label(
            self.root, text="📋  QUIZ HISTORY",
            font=("Helvetica", 18, "bold"),
            bg=BG_DARK, fg=GOLD
        ).pack(pady=(20, 10))

        if not self.history:
            tk.Label(
                self.root,
                text="No quiz sessions yet.\nStart your first quiz!",
                font=("Helvetica", 12),
                bg=BG_DARK, fg=TEXT_DIM,
                justify="center"
            ).pack(pady=40)
        else:
            #header
            hdr = tk.Frame(self.root, bg=BG_PANEL)
            hdr.pack(fill="x", padx=24)
            for col, w in [("Date", 18), ("Score", 8), ("%", 8), ("Grade", 6)]:
                tk.Label(
                    hdr, text=col,
                    font=("Helvetica", 9, "bold"),
                    bg=BG_PANEL, fg=TEXT_DIM,
                    width=w, anchor="w", pady=4
                ).pack(side="left")

            tk.Frame(self.root, bg=PURPLE_LIGHT, height=1).pack(
                fill="x", padx=24)

            #rows
            for h in reversed(self.history):
                grade  = h.get("grade", "?")
                gcolor = get_grade_color(grade)
                row    = tk.Frame(self.root, bg=BG_DARK)
                row.pack(fill="x", padx=24, pady=1)

                for val, w, color in [
                    (h["date"],               18, TEXT_DIM),
                    (f"{h['score']}/{h['total']}", 8, TEXT_WHITE),
                    (f"{h['percent']}%",       8, gcolor),
                    (grade,                    6, gcolor),
                ]:
                    tk.Label(
                        row, text=val,
                        font=("Helvetica", 9),
                        bg=BG_DARK, fg=color,
                        width=w, anchor="w"
                    ).pack(side="left")

                tk.Frame(self.root, bg=BG_PANEL, height=1).pack(
                    fill="x", padx=24)

        tk.Button(
            self.root, text="🏠  BACK TO HOME",
            font=("Helvetica", 11, "bold"),
            bg=BG_PANEL, fg=TEXT_WHITE,
            relief="flat", pady=10,
            command=self._build_home_screen
        ).pack(fill="x", padx=60, pady=20)

        tk.Frame(self.root, bg=GOLD, height=4).pack(
            fill="x", side="bottom")


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------

def main():
    root = tk.Tk()
    QuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()