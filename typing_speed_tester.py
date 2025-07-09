#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 16:06:34 2025

@author: nazar
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import json
import random
import os

USERS_FILE = "typing_users.json"

sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a great programming language for beginners.",
    "Typing fast helps improve productivity and focus.",
    "Practice makes perfect in the world of coding.",
    "Always comment your code to help others understand."
]

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

class TypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Tester ⌨️")

        self.users = load_users()
        self.current_user = None

        self.login_screen()

    def login_screen(self):
        self.clear()
        tk.Label(self.root, text="Login or Signup", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Login", width=20, command=self.login).pack(pady=5)
        tk.Button(self.root, text="Signup", width=20, command=self.signup).pack(pady=5)

    def login(self):
        username = simpledialog.askstring("Login", "Username:")
        password = simpledialog.askstring("Login", "Password:", show="*")
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = self.users[username]
            self.typing_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def signup(self):
        username = simpledialog.askstring("Signup", "Choose a username:")
        if username in self.users:
            messagebox.showerror("Error", "Username already exists.")
            return
        password = simpledialog.askstring("Signup", "Choose a password:", show="*")
        self.users[username] = {
            "password": password,
            "best_wpm": 0
        }
        save_users(self.users)
        messagebox.showinfo("Success", "Account created!")
        self.login_screen()

    def typing_screen(self):
        self.clear()
        self.sentence = random.choice(sentences)
        self.start_time = None

        tk.Label(self.root, text="Typing Speed Tester", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Type the sentence below:", font=("Arial", 12)).pack()

        self.sentence_label = tk.Label(self.root, text=self.sentence, wraplength=500, font=("Arial", 12), fg="blue")
        self.sentence_label.pack(pady=10)

        self.entry = tk.Text(self.root, height=4, width=60)
        self.entry.pack()
        self.entry.bind("<FocusIn>", self.start_timer)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)

        tk.Button(self.root, text="Submit", command=self.calculate_speed).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

    def start_timer(self, event):
        if not self.start_time:
            self.start_time = time.time()

    def calculate_speed(self):
        typed = self.entry.get("1.0", tk.END).strip()
        end_time = time.time()
        time_taken = end_time - self.start_time if self.start_time else 1

        word_count = len(typed.split())
        wpm = round(word_count / (time_taken / 60), 2)

        accuracy = self.calculate_accuracy(self.sentence, typed)

        result = f"🕒 Time: {round(time_taken, 2)}s | 📝 WPM: {wpm} | 🎯 Accuracy: {accuracy}%"
        self.result_label.config(text=result)

        if wpm > self.current_user.get("best_wpm", 0):
            self.current_user["best_wpm"] = wpm
            save_users(self.users)
            result += "\n🏆 New Best Score!"

        messagebox.showinfo("Result", result)

    def calculate_accuracy(self, original, typed):
        original_words = original.split()
        typed_words = typed.split()
        correct = sum(1 for o, t in zip(original_words, typed_words) if o == t)
        return round((correct / len(original_words)) * 100, 2) if original_words else 0

    def logout(self):
        self.current_user = None
        self.start_time = None
        self.login_screen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingApp(root)
    root.mainloop()
