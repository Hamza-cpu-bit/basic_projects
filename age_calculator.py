import tkinter as tk
from tkinter import messagebox
import datetime
import json
import os

# File to store user accounts
DATA_FILE = "users.json"

# Load users
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save users
def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Calculate age and birthday info
def calculate_info(name, dob_str):
    today = datetime.date.today()
    dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
    age_years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    # Next birthday
    next_birthday = dob.replace(year=today.year)
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)

    days_left = (next_birthday - today).days

    # Birthday today?
    is_birthday = today.month == dob.month and today.day == dob.day

    return age_years, days_left, is_birthday

# Login and calculate
def login():
    username = username_entry.get()
    password = password_entry.get()

    users = load_users()

    if username in users and users[username]["password"] == password:
        dob_str = users[username]["birthdate"]
        age, days_left, is_birthday = calculate_info(username, dob_str)

        if is_birthday:
            messagebox.showinfo("🎉 Birthday!", f"🎂 Happy Birthday, {username}!\nYou are now {age} years old.")
        else:
            messagebox.showinfo("Age Info", f"👤 {username}\nAge: {age} years\n🎉 Days until next birthday: {days_left}")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Register new user
def register():
    username = username_entry.get()
    password = password_entry.get()
    dob_str = dob_entry.get()

    try:
        datetime.datetime.strptime(dob_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Date", "Date must be in YYYY-MM-DD format.")
        return

    users = load_users()

    if username in users:
        messagebox.showerror("User Exists", "This username already exists.")
    else:
        users[username] = {"password": password, "birthdate": dob_str}
        save_users(users)
        messagebox.showinfo("Registered", "Account created successfully!")

# GUI setup
root = tk.Tk()
root.title("🎂 Age & Birthday App")

tk.Label(root, text="Username").grid(row=0, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)

tk.Label(root, text="Password").grid(row=1, column=0)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1)

tk.Label(root, text="Birthdate (YYYY-MM-DD)").grid(row=2, column=0)
dob_entry = tk.Entry(root)
dob_entry.grid(row=2, column=1)

tk.Button(root, text="Login & Check Age", command=login).grid(row=3, column=0, columnspan=2, pady=5)
tk.Button(root, text="Register New User", command=register).grid(row=4, column=0, columnspan=2)

root.mainloop()
