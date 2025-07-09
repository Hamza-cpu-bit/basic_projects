#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 11:29:59 2025

@author: nazar
"""

import tkinter as tk
from tkinter import filedialog

def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        with open(file, "w") as f:
            f.write(text.get("1.0", tk.END))

def open_file():
    file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file:
        with open(file, "r") as f:
            content = f.read()
        text.delete("1.0", tk.END)
        text.insert(tk.END, content)

root = tk.Tk()
root.title("📝 Mini Notepad")
text = tk.Text(root, wrap="word")
text.pack(expand=True, fill="both")

menu = tk.Menu(root)
file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
menu.add_cascade(label="File", menu=file_menu)

root.config(menu=menu)
root.mainloop()
