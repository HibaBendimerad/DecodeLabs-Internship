"""
Project 3: Random Password Generator (CLI Version)
DecodeLabs Industrial Training Kit - Python Programming

This program generates cryptographically secure passwords.
It applies the IPO model:
- Input: password length + character set options (validated)
- Process: secrets.choice() + ''.join() to build the password
- Output: the password + entropy score (bits)

Key concepts: string module, secrets module, ''.join(),
              entropy calculation (E = L x log2(R)),
              guaranteed complexity, JSON history.
"""

import string
import secrets
import math
import json
import os

HISTORY_FILE = "password_history.json"


# ---------------------------------------------------------------
# DATA LOGIC
# ---------------------------------------------------------------

def load_history():
    """Load previously generated passwords from disk."""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_history(history):
    """Save password history to disk."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def build_alphabet(use_letters, use_digits, use_symbols):
    """
    Process step: pool available character sets.
    Professional engineers never hard-code character arrays —
    they use the string module for locale-independent consistency.
    """
    alphabet = ""
    if use_letters:
        alphabet += string.ascii_letters   # a-z + A-Z (52 chars)
    if use_digits:
        alphabet += string.digits          # 0-9     (10 chars)
    if use_symbols:
        alphabet += string.punctuation     # !"#$%... (32 chars)
    return alphabet


def calculate_entropy(length, pool_size):
    """
    Phase 3 — Mathematical provision of security.
    E = L x log2(R)
    E : entropy in bits
    L : password length
    R : character pool size
    """
    if pool_size < 2:
        return 0.0
    return round(length * math.log2(pool_size), 2)


def strength_label(entropy):
    """Convert entropy bits to a human-readable strength label."""
    if entropy < 28:
        return "❌ Very Weak"
    elif entropy < 36:
        return "⚠️  Weak"
    elif entropy < 60:
        return "🟡 Fair"
    elif entropy < 80:
        return "🟢 Strong"
    else:
        return "🔒 Very Strong"


def generate_password(length, alphabet):
    """
    Core engine: build the password using secrets.choice() + ''.join().

    WHY secrets over random?
    - random uses Mersenne Twister (seeded by system time → predictable)
    - secrets taps into OS hardware-level entropy (unpredictable)

    WHY ''.join() over += ?
    - += creates a new string object on every iteration → O(N²) memory
    - ''.join() allocates memory exactly once → O(N) — enterprise standard
    """
    #Step 1 — guarantee at least one character from each active set
    guaranteed = []
    if any(c in string.ascii_letters for c in alphabet):
        guaranteed.append(secrets.choice(string.ascii_letters))
    if any(c in string.digits for c in alphabet):
        guaranteed.append(secrets.choice(string.digits))
    if any(c in string.punctuation for c in alphabet):
        guaranteed.append(secrets.choice(string.punctuation))

    #Step 2 — fill the rest randomly from the full alphabet
    remaining = length - len(guaranteed)
    if remaining < 0:
        remaining = 0
    random_chars = [secrets.choice(alphabet) for _ in range(remaining)]

    #Step 3 — merge and shuffle so guaranteed chars aren't always first
    all_chars = guaranteed + random_chars
    secrets.SystemRandom().shuffle(all_chars)

    # tep 4 — join into a single string (O(N) — the professional approach)
    return ''.join(all_chars)


def show_menu():
    print("\n=== PASSWORD GENERATOR ===")
    print("1. Generate a password")
    print("2. View history")
    print("3. Clear history")
    print("4. Exit")


# ---------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------

def main():
    history = load_history()

    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":

            # --- INPUT: length (with validation) ---
            try:
                length = int(input("Password length (min 8, max 128): ").strip())
                if not (8 <= length <= 128):
                    print("⚠️  Length must be between 8 and 128.\n")
                    continue
            except ValueError:
                print("⚠️  Please enter a valid integer.\n")
                continue

            # --- INPUT: character set options ---
            use_letters = input("Include letters? (y/n): ").strip().lower() != "n"
            use_digits  = input("Include digits?  (y/n): ").strip().lower() != "n"
            use_symbols = input("Include symbols? (y/n): ").strip().lower() == "y"

            alphabet = build_alphabet(use_letters, use_digits, use_symbols)

            if not alphabet:
                print("⚠️  You must include at least one character set.\n")
                continue

            # --- PROCESS: generate + calculate entropy ---
            password = generate_password(length, alphabet)
            entropy  = calculate_entropy(length, len(alphabet))
            strength = strength_label(entropy)

            # --- OUTPUT ---
            print("\n" + "─" * 50)
            print(f"  🔑 Password : {password}")
            print(f"  📊 Entropy  : {entropy} bits")
            print(f"  🛡️  Strength : {strength}")
            print(f"  🔤 Pool size: {len(alphabet)} characters")
            print("─" * 50 + "\n")

            #save to history
            history.append({
                "password": password,
                "length":   length,
                "entropy":  entropy,
                "strength": strength
            })
            save_history(history)

        elif choice == "2":
            if not history:
                print("\nNo passwords generated yet.\n")
            else:
                print("\n--- PASSWORD HISTORY ---")
                for i, h in enumerate(history, 1):
                    print(f"  {i:>2}. {h['password']:<30}"
                          f"  {h['entropy']} bits  {h['strength']}")
                print()

        elif choice == "3":
            history = []
            save_history(history)
            print("History cleared.\n")

        elif choice == "4":
            #SENTINEL / KILL SWITCH
            print(f"\nGoodbye! {len(history)} password(s) in history.")
            break

        else:
            print("Invalid option. Please choose between 1 and 4.\n")


if __name__ == "__main__":
    main()