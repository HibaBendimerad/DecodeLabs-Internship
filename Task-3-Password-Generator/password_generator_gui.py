"""
Project 3: Random Password Generator (GUI Version - Cyber/Futuristic Design)
DecodeLabs Industrial Training Kit - Python Programming

Same data logic as CLI version (secrets, string, entropy, JSON).
"""

import string
import secrets
import math
import json
import os
import tkinter as tk
from tkinter import messagebox

HISTORY_FILE = "password_history.json"

# ---------------------------------------------------------------
# CYBER COLOUR PALETTE
# ---------------------------------------------------------------
BG_BLACK     = "#0A0A0F"   # near-black background
BG_PANEL     = "#0F1117"   # slightly lighter panels
BG_HIGHLIGHT = "#141820"   # row highlight
NEON_GREEN   = "#00FF41"   # matrix green (main text)
NEON_CYAN    = "#00D4FF"   # cyan accent (titles, labels)
NEON_RED     = "#FF2D55"   # red accent (warnings, weak)
NEON_YELLOW  = "#FFD60A"   # yellow (fair strength)
NEON_PURPLE  = "#BF5FFF"   # purple (headers)
DIM_GREEN    = "#004D18"   # dimmed green (borders)
DIM_GREY     = "#2A2A3A"   # separator lines
TEXT_DIM     = "#4A5568"   # muted text

STRENGTH_COLORS = {
    "Very Weak":   NEON_RED,
    "Weak":        "#FF6B35",
    "Fair":        NEON_YELLOW,
    "Strong":      NEON_GREEN,
    "Very Strong": NEON_CYAN,
}


# ---------------------------------------------------------------
# DATA LOGIC  
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


def build_alphabet(use_letters, use_digits, use_symbols):
    alphabet = ""
    if use_letters:
        alphabet += string.ascii_letters
    if use_digits:
        alphabet += string.digits
    if use_symbols:
        alphabet += string.punctuation
    return alphabet


def calculate_entropy(length, pool_size):
    if pool_size < 2:
        return 0.0
    return round(length * math.log2(pool_size), 2)


def strength_label(entropy):
    if entropy < 28:   return "Very Weak"
    elif entropy < 36: return "Weak"
    elif entropy < 60: return "Fair"
    elif entropy < 80: return "Strong"
    else:              return "Very Strong"


def generate_password(length, alphabet):
    guaranteed = []
    if any(c in string.ascii_letters for c in alphabet):
        guaranteed.append(secrets.choice(string.ascii_letters))
    if any(c in string.digits for c in alphabet):
        guaranteed.append(secrets.choice(string.digits))
    if any(c in string.punctuation for c in alphabet):
        guaranteed.append(secrets.choice(string.punctuation))

    remaining    = max(0, length - len(guaranteed))
    random_chars = [secrets.choice(alphabet) for _ in range(remaining)]
    all_chars    = guaranteed + random_chars
    secrets.SystemRandom().shuffle(all_chars)
    return ''.join(all_chars)


# ---------------------------------------------------------------
# GUI APPLICATION 
# ---------------------------------------------------------------

class PasswordApp:

    def __init__(self, root):
        self.root = root
        self.root.title("[ PASSWORD GENERATOR v3.0 ] — DecodeLabs Security")
        self.root.geometry("560x780")
        self.root.configure(bg=BG_BLACK)
        self.root.resizable(False, False)

        self.history     = load_history()
        self.last_pw     = ""
        self.blink_state = True

        self.var_letters = tk.BooleanVar(value=True)
        self.var_digits  = tk.BooleanVar(value=True)
        self.var_symbols = tk.BooleanVar(value=False)

        self._build_widgets()
        self._refresh_history()
        self._blink_cursor()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # -----------------------------------------------------------
    # KILL SWITCH
    # -----------------------------------------------------------

    def _on_close(self):
        n = len(self.history)
        messagebox.showinfo(
            "[ SESSION TERMINATED ]",
            f"SYSTEM SHUTDOWN\n\n"
            f"Passwords generated : {n}\n"
            f"History persisted   : password_history.json\n\n"
            f"— DecodeLabs Security Engine —"
        )
        self.root.destroy()

    # -----------------------------------------------------------
    # BLINKING CURSOR EFFECT
    # -----------------------------------------------------------

    def _blink_cursor(self):
        """Simulates a terminal blinking cursor on the title."""
        self.blink_state = not self.blink_state
        cursor = "█" if self.blink_state else " "
        self.cursor_label.configure(text=cursor)
        self.root.after(500, self._blink_cursor)

    # -----------------------------------------------------------
    # CYBER DIVIDER HELPER
    # -----------------------------------------------------------

    def _cyber_divider(self, parent, label=""):
        """Draws a ─── LABEL ─── style divider."""
        frame = tk.Frame(parent, bg=BG_BLACK)
        frame.pack(fill="x", padx=16, pady=(10, 4))

        tk.Frame(frame, bg=DIM_GREEN, height=1).pack(
            side="left", fill="x", expand=True)

        if label:
            tk.Label(
                frame,
                text=f"  {label}  ",
                font=("Courier", 8, "bold"),
                bg=BG_BLACK, fg=NEON_CYAN
            ).pack(side="left")

        tk.Frame(frame, bg=DIM_GREEN, height=1).pack(
            side="left", fill="x", expand=True)

    # -----------------------------------------------------------
    # WIDGET CONSTRUCTION
    # -----------------------------------------------------------

    def _build_widgets(self):

        # ── CYBER HEADER ───────────────────────────────────────
        header = tk.Frame(self.root, bg=BG_BLACK)
        header.pack(fill="x", padx=16, pady=(16, 0))

        # top scanline
        tk.Frame(self.root, bg=NEON_CYAN, height=1).pack(
            fill="x", padx=16)

        title_row = tk.Frame(self.root, bg=BG_PANEL)
        title_row.pack(fill="x", padx=16)

        tk.Label(
            title_row,
            text="[ RANDOM PASSWORD GENERATOR ]",
            font=("Courier", 14, "bold"),
            bg=BG_PANEL, fg=NEON_GREEN
        ).pack(side="left", padx=10, pady=8)

        self.cursor_label = tk.Label(
            title_row, text="█",
            font=("Courier", 14, "bold"),
            bg=BG_PANEL, fg=NEON_GREEN
        )
        self.cursor_label.pack(side="left")

        tk.Label(
            title_row,
            text="v3.0",
            font=("Courier", 9),
            bg=BG_PANEL, fg=NEON_CYAN
        ).pack(side="right", padx=10)

        tk.Frame(self.root, bg=NEON_CYAN, height=1).pack(
            fill="x", padx=16)

        # boot message
        tk.Label(
            self.root,
            text="> Initializing security engine... OK\n"
                 "> Loading entropy sources... READY",
            font=("Courier", 8),
            bg=BG_BLACK, fg=DIM_GREEN,
            justify="left"
        ).pack(anchor="w", padx=20, pady=(6, 0))

        # ── CONFIGURATION ──────────────────────────────────────
        self._cyber_divider(self.root, "// CONFIGURATION")

        config_panel = tk.Frame(
            self.root, bg=BG_PANEL,
            highlightbackground=DIM_GREEN,
            highlightthickness=1
        )
        config_panel.pack(fill="x", padx=16, pady=(0, 0))

        # length slider row
        len_row = tk.Frame(config_panel, bg=BG_PANEL)
        len_row.pack(fill="x", padx=10, pady=(10, 4))

        tk.Label(
            len_row, text="> LENGTH :",
            font=("Courier", 9, "bold"),
            bg=BG_PANEL, fg=NEON_CYAN
        ).pack(side="left")

        self.length_var = tk.IntVar(value=16)
        tk.Scale(
            len_row,
            from_=8, to=64,
            orient="horizontal",
            variable=self.length_var,
            bg=BG_PANEL, fg=NEON_GREEN,
            troughcolor=DIM_GREY,
            highlightthickness=0,
            activebackground=NEON_GREEN,
            font=("Courier", 8),
            command=lambda v: self.length_val.configure(
                text=f"[ {int(float(v)):>3} ]")
        ).pack(side="left", fill="x", expand=True, padx=(8, 8))

        self.length_val = tk.Label(
            len_row, text="[  16 ]",
            font=("Courier", 10, "bold"),
            bg=BG_PANEL, fg=NEON_GREEN
        )
        self.length_val.pack(side="left")

        # charset checkboxes
        cb_row = tk.Frame(config_panel, bg=BG_PANEL)
        cb_row.pack(fill="x", padx=10, pady=(4, 10))

        tk.Label(
            cb_row, text="> CHARSET :",
            font=("Courier", 9, "bold"),
            bg=BG_PANEL, fg=NEON_CYAN
        ).pack(side="left")

        for text, var in [
            ("[A-Za-z]", self.var_letters),
            ("[0-9]",    self.var_digits),
            ("[!@#$]",   self.var_symbols),
        ]:
            tk.Checkbutton(
                cb_row, text=text,
                variable=var,
                font=("Courier", 9),
                bg=BG_PANEL, fg=NEON_GREEN,
                selectcolor=BG_BLACK,
                activebackground=BG_PANEL,
                activeforeground=NEON_GREEN
            ).pack(side="left", padx=(10, 0))

        # ── GENERATE BUTTON ────────────────────────────────────
        tk.Button(
            self.root,
            text="⚡  EXECUTE // GENERATE SECURE PASSWORD",
            font=("Courier", 10, "bold"),
            bg=DIM_GREEN, fg=NEON_GREEN,
            relief="flat", pady=10,
            activebackground=NEON_GREEN,
            activeforeground=BG_BLACK,
            command=self._on_generate
        ).pack(fill="x", padx=16, pady=(10, 0))

        # ── PASSWORD OUTPUT ────────────────────────────────────
        self._cyber_divider(self.root, "// OUTPUT")

        pw_panel = tk.Frame(
            self.root, bg=BG_PANEL,
            highlightbackground=NEON_GREEN,
            highlightthickness=1
        )
        pw_panel.pack(fill="x", padx=16)

        top_row = tk.Frame(pw_panel, bg=BG_PANEL)
        top_row.pack(fill="x", padx=8, pady=(6, 0))

        tk.Label(
            top_row, text="> CREDENTIAL :",
            font=("Courier", 8),
            bg=BG_PANEL, fg=NEON_CYAN
        ).pack(side="left")

        self.pw_label = tk.Label(
            pw_panel,
            text="_ _ _ AWAITING INPUT _ _ _",
            font=("Courier", 13, "bold"),
            bg=BG_PANEL, fg=TEXT_DIM,
            pady=10, wraplength=500
        )
        self.pw_label.pack(fill="x", padx=8)

        # copy button
        tk.Button(
            self.root,
            text="[ COPY TO CLIPBOARD ]",
            font=("Courier", 9, "bold"),
            bg=BG_BLACK, fg=NEON_CYAN,
            relief="flat", pady=5,
            highlightthickness=1,
            highlightbackground=NEON_CYAN,
            activebackground=NEON_CYAN,
            activeforeground=BG_BLACK,
            command=self._on_copy
        ).pack(fill="x", padx=16, pady=(6, 0))

        # ── SECURITY ANALYSIS ──────────────────────────────────
        self._cyber_divider(self.root, "// SECURITY ANALYSIS")

        analysis_panel = tk.Frame(
            self.root, bg=BG_PANEL,
            highlightbackground=DIM_GREEN,
            highlightthickness=1
        )
        analysis_panel.pack(fill="x", padx=16)

        for key, attr in [
            ("ENTROPY  (bits)", "entropy_lbl"),
            ("STRENGTH",        "strength_lbl"),
            ("POOL SIZE",       "pool_lbl"),
        ]:
            row = tk.Frame(analysis_panel, bg=BG_PANEL)
            row.pack(fill="x", pady=1)

            tk.Label(
                row, text=f"  > {key:<18}:",
                font=("Courier", 9),
                bg=BG_PANEL, fg=NEON_CYAN,
                width=24, anchor="w"
            ).pack(side="left")

            lbl = tk.Label(
                row, text="—",
                font=("Courier", 9, "bold"),
                bg=BG_PANEL, fg=NEON_GREEN,
                anchor="w"
            )
            lbl.pack(side="left", fill="x", expand=True)
            setattr(self, attr, lbl)

            tk.Frame(
                analysis_panel, bg=DIM_GREY, height=1
            ).pack(fill="x")

        #entropy meter
        tk.Label(
            self.root, text="  > ENTROPY_METER :",
            font=("Courier", 8),
            bg=BG_BLACK, fg=NEON_CYAN
        ).pack(anchor="w", padx=16, pady=(8, 2))

        self.meter_canvas = tk.Canvas(
            self.root, bg=BG_PANEL,
            highlightthickness=1,
            highlightbackground=DIM_GREEN,
            height=24
        )
        self.meter_canvas.pack(fill="x", padx=16)

        # ── HISTORY ────────────────────────────────────────────
        self._cyber_divider(self.root, "// HISTORY LOG")

        hist_container = tk.Frame(
            self.root, bg=BG_PANEL,
            highlightbackground=DIM_GREEN,
            highlightthickness=1
        )
        hist_container.pack(
            fill="both", expand=True, padx=16)

        self.hist_canvas = tk.Canvas(
            hist_container, bg=BG_PANEL,
            highlightthickness=0, height=110)
        sb = tk.Scrollbar(
            hist_container, orient="vertical",
            command=self.hist_canvas.yview,
            bg=BG_PANEL, troughcolor=DIM_GREY)
        self.hist_canvas.configure(yscrollcommand=sb.set)
        self.hist_canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.hist_frame = tk.Frame(self.hist_canvas, bg=BG_PANEL)
        self._cw = self.hist_canvas.create_window(
            (0, 0), window=self.hist_frame, anchor="nw")

        self.hist_frame.bind(
            "<Configure>",
            lambda e: self.hist_canvas.configure(
                scrollregion=self.hist_canvas.bbox("all")))
        self.hist_canvas.bind(
            "<Configure>",
            lambda e: self.hist_canvas.itemconfig(
                self._cw, width=e.width))

        #clear button
        tk.Button(
            self.root,
            text="[ PURGE HISTORY LOG ]",
            font=("Courier", 9, "bold"),
            bg=BG_BLACK, fg=NEON_RED,
            relief="flat", pady=5,
            highlightthickness=1,
            highlightbackground=NEON_RED,
            activebackground=NEON_RED,
            activeforeground=BG_BLACK,
            command=self._on_clear
        ).pack(fill="x", padx=16, pady=(6, 0))

        #bottom scanline
        tk.Frame(self.root, bg=NEON_CYAN, height=1).pack(
            fill="x", padx=16, pady=(8, 0))

        #status bar
        self.status_var = tk.StringVar(
            value="> SYSTEM READY // AWAITING COMMAND")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Courier", 8),
            bg=BG_BLACK, fg=DIM_GREEN
        ).pack(anchor="w", padx=20, pady=(4, 8))

    # -----------------------------------------------------------
    # CALLBACKS
    # -----------------------------------------------------------

    def _on_generate(self):
        length = self.length_var.get()

        alphabet = build_alphabet(
            self.var_letters.get(),
            self.var_digits.get(),
            self.var_symbols.get()
        )

        if not alphabet:
            messagebox.showerror(
                "[ ERROR ]",
                "FATAL: No character set selected.\nSelect at least one charset.")
            return

        password = generate_password(length, alphabet)
        entropy  = calculate_entropy(length, len(alphabet))
        strength = strength_label(entropy)
        color    = STRENGTH_COLORS.get(strength, NEON_GREEN)

        self.last_pw = password

        self.pw_label.configure(text=password, fg=NEON_GREEN)
        self.entropy_lbl.configure(text=f"{entropy} bits")
        self.strength_lbl.configure(text=strength, fg=color)
        self.pool_lbl.configure(text=f"{len(alphabet)} characters")

        self._draw_meter(entropy, color)

        self.history.append({
            "password": password,
            "length":   length,
            "entropy":  entropy,
            "strength": strength
        })
        save_history(self.history)
        self._refresh_history()

        self.status_var.set(
            f"> CREDENTIAL GENERATED // {entropy} bits // {strength.upper()}")

    def _on_copy(self):
        if not self.last_pw:
            messagebox.showinfo("[ INFO ]", "No password generated yet.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.last_pw)
        self.status_var.set("> CREDENTIAL COPIED TO CLIPBOARD // OK")

    def _on_clear(self):
        if not self.history:
            return
        if messagebox.askyesno(
                "[ CONFIRM ]",
                "PURGE ALL HISTORY LOGS?\nThis action cannot be undone."):
            self.history = []
            save_history(self.history)
            self._refresh_history()
            self.status_var.set("> HISTORY LOG PURGED // OK")

    # -----------------------------------------------------------
    # DRAWING
    # -----------------------------------------------------------

    def _draw_meter(self, entropy, color):
        self.meter_canvas.delete("all")
        w      = self.meter_canvas.winfo_width() or 500
        max_e  = 130.0
        fill_w = int(min(entropy / max_e, 1.0) * (w - 4))

        # dark track
        self.meter_canvas.create_rectangle(
            2, 2, w - 2, 22,
            fill=DIM_GREY, outline=DIM_GREEN)

        # glowing bar (two layers for glow effect)
        if fill_w > 0:
            self.meter_canvas.create_rectangle(
                2, 2, 2 + fill_w, 22,
                fill=color, outline="")
            # inner bright strip (glow illusion)
            self.meter_canvas.create_rectangle(
                2, 6, 2 + fill_w, 10,
                fill="#FFFFFF" if color == NEON_GREEN else color,
                stipple="gray50", outline="")

        # segment marks every 10%
        for pct in range(10, 100, 10):
            x = int(pct / 100 * (w - 4)) + 2
            self.meter_canvas.create_line(
                x, 2, x, 22, fill=DIM_GREY, width=1)

        # label
        self.meter_canvas.create_text(
            w // 2, 12,
            text=f"  {entropy} bits  ",
            fill=BG_BLACK if fill_w > w // 2 else color,
            font=("Courier", 8, "bold"))

    def _refresh_history(self):
        for w in self.hist_frame.winfo_children():
            w.destroy()

        if not self.history:
            tk.Label(
                self.hist_frame,
                text="> NO ENTRIES IN LOG",
                font=("Courier", 8),
                bg=BG_PANEL, fg=TEXT_DIM
            ).pack(anchor="w", padx=8, pady=4)
            return

        for i, h in enumerate(reversed(self.history), 1):
            color = STRENGTH_COLORS.get(h["strength"], NEON_GREEN)
            row   = tk.Frame(self.hist_frame, bg=BG_PANEL)
            row.pack(fill="x")

            tk.Label(
                row, text=f"  [{i:>2}]",
                font=("Courier", 8),
                bg=BG_PANEL, fg=TEXT_DIM, width=6
            ).pack(side="left")

            tk.Label(
                row, text=h["password"],
                font=("Courier", 9),
                bg=BG_PANEL, fg=NEON_GREEN
            ).pack(side="left", padx=(0, 10))

            tk.Label(
                row, text=f"{h['entropy']}b",
                font=("Courier", 8, "bold"),
                bg=BG_PANEL, fg=color
            ).pack(side="right", padx=6)

            tk.Frame(
                self.hist_frame, bg=DIM_GREY, height=1
            ).pack(fill="x")


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------

def main():
    root = tk.Tk()
    PasswordApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()