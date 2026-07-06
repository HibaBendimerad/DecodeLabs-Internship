# Task 3 — Random Password Generator

> **DecodeLabs Python Programming Internship | Batch 2026**
> Project 3 of the Industrial Training Kit — Security Phase

---

## Project Goal

Build a cryptographically secure password generator that asks the user
for a length and character set options, then generates an unpredictable
password — and mathematically proves its strength using entropy calculation.

---

## Features

| Feature | CLI | GUI |
|---------|:---:|:---:|
| Choose password length (8–128) | ✅ | ✅ (slider) |
| Toggle letters / digits / symbols | ✅ | ✅ (checkboxes) |
| Cryptographically secure generation (`secrets`) | ✅ | ✅ |
| Guaranteed complexity (at least 1 of each set) | ✅ | ✅ |
| Entropy calculation `E = L × log₂(R)` | ✅ | ✅ |
| Strength label (Very Weak → Very Strong) | ✅ | ✅ |
| Live entropy meter bar | — | ✅ |
| Copy to clipboard | — | ✅ |
| Password history (JSON persistence) | ✅ | ✅ |
| Kill switch with session summary | ✅ | ✅ |

---

## Concepts Applied

| Concept | Where it appears |
|---------|-----------------|
| **`string` module** | `string.ascii_letters`, `string.digits`, `string.punctuation` — professional character pools |
| **`secrets` module** | `secrets.choice()` — cryptographically secure, replaces `random` |
| **`''.join()`** | O(N) string assembly — enterprise-grade over `+=` which is O(N²) |
| **Entropy formula** | `E = L × log₂(R)` via `math.log2()` |
| **Guaranteed complexity** | `any(c in string.digits for c in alphabet)` |
| **`secrets.SystemRandom().shuffle()`** | Cryptographically secure shuffle of guaranteed chars |
| **JSON persistence** | Password history saved to `password_history.json` |
| **IPO model** | Input (length + options) → Process (generate + entropy) → Output (password + meter) |

---

## Why `secrets` over `random`?

| | `random` | `secrets` |
|---|---|---|
| Algorithm | Mersenne Twister (deterministic) | OS hardware entropy |
| Predictable? | ✅ Yes — if seed is known | ❌ No — true randomness |
| Use case | Simulations, games | Passwords, tokens, keys |
| NIST compliant? | ❌ No | ✅ Yes |

---

## The Entropy Formula

```
E = L × log₂(R)

E = entropy in bits (higher = more secure)
L = password length
R = character pool size
```

| Pool | R | 16-char entropy |
|------|---|----------------|
| Letters only | 52 | 90.6 bits |
| Letters + digits | 62 | 95.6 bits |
| Full (+ symbols) | 94 | 104.9 bits ✅ NIST |

---

##  How to Run

```bash
# Command-line version
python3 password_generator.py

# Graphical version
python3 password_generator_gui.py
```

---

##  File Structure

```
Task-3-Password-Generator/
├── password_generator.py       # Command-line version
├── password_generator_gui.py   # Graphical version with entropy meter
├── password_history.json       # Auto-generated — do NOT commit
└── README.md                   # This file
```

---

*Built with Python 3 | DecodeLabs Internship Batch 2026*