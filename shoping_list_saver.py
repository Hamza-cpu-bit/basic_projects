#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 16:24:00 2025

@author: nazar
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import os

FILE = "shopping_list.txt"

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_data(data):
    with open(FILE, "w") as f:
        for item in data:
            f.write(item + "\n")

class ShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛒 Shopping List App (Text File)")
        self.data = load_data()
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="🛍️ My Shopping List", font=("Arial", 16)).pack(pady=10)
        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(pady=10)

        self.update_list()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Add Item", command=self.add_item).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Delete Item", command=self.delete_item).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Clear All", command=self.clear_all).grid(row=0, column=2, padx=5)

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for item in self.data:
            self.listbox.insert(tk.END, item)

    def add_item(self):
        item = simpledialog.askstring("New Item", "Enter item:")
        if item:
            self.data.append(item)
            save_data(self.data)
            self.update_list()

    def delete_item(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            del self.data[index]
            save_data(self.data)
            self.update_list()
        else:
            messagebox.showwarning("No selection", "Please select an item to delete.")

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear all items?"):
            self.data = []
            save_data(self.data)
            self.update_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingApp(root)
    root.mainloop()


