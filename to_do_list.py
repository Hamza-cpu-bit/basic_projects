import tkinter as tk
from tkinter import messagebox
import json
import os

USERS_FILE = "todo_users.json"

def load_data():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def register():
    username = user_entry.get()
    password = pass_entry.get()
    if username and password:
        users = load_data()
        if username in users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            users[username] = {"password": password, "tasks": []}
            save_data(users)
            messagebox.showinfo("Success", "User registered!")
    else:
        messagebox.showerror("Error", "Fill in all fields.")

def login():
    global current_user
    username = user_entry.get()
    password = pass_entry.get()
    users = load_data()
    if username in users and users[username]["password"] == password:
        current_user = username
        login_frame.pack_forget()
        show_task_manager(users[username]["tasks"])
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

def show_task_manager(user_tasks):
    global listbox
    listbox = tk.Listbox(root, width=40, height=10)
    listbox.pack()
    for task in user_tasks:
        listbox.insert(tk.END, task)

    entry.pack()
    add_btn.pack()
    del_btn.pack()

def add_task():
    task = entry.get()
    if task:
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        users = load_data()
        users[current_user]["tasks"].append(task)
        save_data(users)

def delete_task():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        listbox.delete(index)
        users = load_data()
        users[current_user]["tasks"].pop(index)
        save_data(users)

root = tk.Tk()
root.title("To-Do List with Login")

current_user = None

login_frame = tk.Frame(root)
login_frame.pack()

tk.Label(login_frame, text="Username").pack()
user_entry = tk.Entry(login_frame)
user_entry.pack()

tk.Label(login_frame, text="Password").pack()
pass_entry = tk.Entry(login_frame, show="*")
pass_entry.pack()

tk.Button(login_frame, text="Register", command=register).pack(pady=2)
tk.Button(login_frame, text="Login", command=login).pack(pady=2)

entry = tk.Entry(root, width=30)
add_btn = tk.Button(root, text="Add Task", command=add_task)
del_btn = tk.Button(root, text="Delete Task", command=delete_task)

root.mainloop()
