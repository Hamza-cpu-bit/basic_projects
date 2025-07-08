#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 17:49:22 2025

@author: nazar
"""

import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import os

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register():
    username = user_entry.get()
    password = pass_entry.get()
    dob = dob_entry.get()
    if username and password and dob:
        users = load_users()
        if username in users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            users[username] = {"password": password, "dob": dob}
            save_users(users)
            messagebox.showinfo("Success", "User registered!")
    else:
        messagebox.showerror("Error", "Please fill all fields.")

def login():
    username = user_entry.get()
    password = pass_entry.get()
    users = load_users()
    if username in users and users[username]["password"] == password:
        dob = users[username]["dob"]
        calculate_age(dob)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

def calculate_age(birthday_str):
    try:
        bday = datetime.strptime(birthday_str, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))
        messagebox.showinfo("Your Age", f"You are {age} years old.")
    except Exception as e:
        messagebox.showerror("Error", "Invalid date format (use YYYY-MM-DD)")

root = tk.Tk()
root.title("Age Calculator with Login")

tk.Label(root, text="Username").pack()
user_entry = tk.Entry(root)
user_entry.pack()

tk.Label(root, text="Password").pack()
pass_entry = tk.Entry(root, show="*")
pass_entry.pack()

tk.Label(root, text="DOB (YYYY-MM-DD)").pack()
dob_entry = tk.Entry(root)
dob_entry.pack()

tk.Button(root, text="Register", command=register).pack(pady=5)
tk.Button(root, text="Login and Calculate Age", command=login).pack(pady=5)

root.mainloop()
