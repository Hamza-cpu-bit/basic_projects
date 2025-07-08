#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 15:20:44 2025

@author: nazar
"""

import tkinter as tk
from tkinter import messagebox
import json
import os
import random

WORDS = [
    "python", "developer", "programming", "function", "variable", "condition", "loop", "integer",
    "string", "boolean", "float", "syntax", "compile", "execute", "error", "exception",
    "list", "tuple", "dictionary", "set", "array", "index", "slice", "class", "object",
    "inheritance", "polymorphism", "encapsulation", "abstraction", "algorithm", "binary",
    "debug", "iterate", "recursion", "stack", "queue", "search", "sort", "merge", "insert",
    "delete", "hash", "graph", "tree", "node", "edge", "depth", "breadth"
]

ACCOUNTS_FILE = "accounts.json"

# --- Account Management ---
def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump({}, f)
    with open(ACCOUNTS_FILE, 'r') as f:
        return json.load(f)

def save_accounts(data):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- GUI Application ---
class WordScrambleApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🔤 Word Scramble Game")
        self.username = None
        self.accounts = load_accounts()
        self.scrambled_word = ""
        self.original_word = ""
        self.score = 0
        self.round = 0
        self.total_rounds = 5

        self.login_screen()

    def login_screen(self):
        self.clear()
        tk.Label(self.master, text="👤 Username").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        tk.Label(self.master, text="🔒 Password").pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        tk.Button(self.master, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.master, text="Sign Up", command=self.signup).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.accounts and self.accounts[username]["password"] == password:
            self.username = username
            self.score = 0
            self.round = 0
            self.start_game()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.accounts:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.accounts[username] = {"password": password, "score": 0}
            save_accounts(self.accounts)
            messagebox.showinfo("Success", "Account created!")

    def start_game(self):
        self.clear()
        self.new_round()

    def new_round(self):
        if self.round >= self.total_rounds:
            self.end_game()
            return

        self.original_word = random.choice(WORDS)
        self.scrambled_word = ''.join(random.sample(self.original_word, len(self.original_word)))
        while self.scrambled_word == self.original_word:
            self.scrambled_word = ''.join(random.sample(self.original_word, len(self.original_word)))

        self.round += 1

        self.clear()
        tk.Label(self.master, text=f"Round {self.round}/{self.total_rounds}", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.master, text=f"Scrambled: {self.scrambled_word}", font=("Arial", 16, "bold")).pack(pady=10)

        self.guess_entry = tk.Entry(self.master)
        self.guess_entry.pack()
        self.guess_entry.focus()

        tk.Button(self.master, text="Submit Guess", command=self.check_guess).pack(pady=10)

    def check_guess(self):
        guess = self.guess_entry.get().strip().lower()
        if guess == self.original_word:
            self.score += 1
            messagebox.showinfo("✅ Correct!", f"Correct! Score: {self.score}")
        else:
            messagebox.showerror("❌ Incorrect", f"Wrong! The word was: {self.original_word}")
        self.new_round()

    def end_game(self):
        self.accounts[self.username]["score"] = self.score
        save_accounts(self.accounts)
        self.clear()
        tk.Label(self.master, text=f"🏁 Game Over!", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.master, text=f"Your Score: {self.score}/{self.total_rounds}", font=("Arial", 14)).pack(pady=5)
        tk.Button(self.master, text="Play Again", command=self.start_game).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.login_screen).pack()

    def clear(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# --- Run ---
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("350x300")
    app = WordScrambleApp(root)
    root.mainloop()



