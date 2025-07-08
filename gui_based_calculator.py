#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 15:15:45 2025

@author: nazar
"""

import tkinter as tk
from math import sin, cos, tan, log, sqrt, pow, radians
from tkinter import messagebox

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        self.expression = ""

        self.input_text = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg="lightgrey")
        input_frame.pack(side=tk.TOP, fill=tk.BOTH)

        input_field = tk.Entry(
            input_frame, font=('Arial', 24), textvariable=self.input_text,
            bd=4, relief=tk.FLAT, justify='right'
        )
        input_field.grid(row=0, column=0, ipady=20, ipadx=8, sticky="we")

        btn_frame = tk.Frame(self.root, bg="lightgrey")
        btn_frame.pack()

        # Buttons layout
        buttons = [
            ['7', '8', '9', '/', 'sqrt'],
            ['4', '5', '6', '*', '^'],
            ['1', '2', '3', '-', 'log'],
            ['0', '.', '(', ')', '+'],
            ['sin', 'cos', 'tan', 'C', '=']
        ]

        for row_index, row in enumerate(buttons):
            for col_index, symbol in enumerate(row):
                btn = tk.Button(
                    btn_frame, text=symbol, font=('Arial', 18), width=6, height=2,
                    command=lambda val=symbol: self.on_click(val)
                )
                btn.grid(row=row_index, column=col_index, padx=2, pady=2)

    def on_click(self, value):
        if value == "C":
            self.expression = ""
            self.input_text.set("")
        elif value == "=":
            try:
                result = self.evaluate_expression(self.expression)
                self.input_text.set(result)
                self.expression = str(result)
            except Exception as e:
                messagebox.showerror("Error", "Invalid Input")
                self.expression = ""
                self.input_text.set("")
        elif value in ["sin", "cos", "tan", "log", "sqrt"]:
            self.expression += f"{value}("
            self.input_text.set(self.expression)
        elif value == "^":
            self.expression += "**"
            self.input_text.set(self.expression)
        else:
            self.expression += str(value)
            self.input_text.set(self.expression)

    def evaluate_expression(self, expr):
        # Replace math function names with proper calls
        expr = expr.replace("sin", "sin(radians")
        expr = expr.replace("cos", "cos(radians")
        expr = expr.replace("tan", "tan(radians")
        expr = expr.replace("log", "log")
        expr = expr.replace("sqrt", "sqrt")

        # Close any unclosed parentheses from trig functions
        open_count = expr.count('(')
        close_count = expr.count(')')
        expr += ')' * (open_count - close_count)

        return eval(expr)

if __name__ == "__main__":
    root = tk.Tk()
    calc = AdvancedCalculator(root)
    root.mainloop()
