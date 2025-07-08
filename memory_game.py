import tkinter as tk
import random
from functools import partial
from tkinter import messagebox

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Memory Game")
        self.root.geometry("400x450")
        self.root.resizable(False, False)

        self.symbols = ['W', 'P', '@', '_', '+', 'L', 'j', '4'] * 2
        self.buttons = []
        self.first_choice = None
        self.second_choice = None
        self.locked = False

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        for i in range(4):
            row = []
            for j in range(4):
                btn = tk.Button(self.frame, text="❓", font=("Arial", 16), width=6, height=3,
                                command=partial(self.reveal_symbol, i, j), bg="lightgray")
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        self.restart_btn = tk.Button(self.root, text="🔁 Restart", command=self.new_game, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.restart_btn.pack(pady=10)

    def new_game(self):
        self.first_choice = None
        self.second_choice = None
        self.locked = False
        self.board = random.sample(self.symbols, len(self.symbols))

        for i in range(4):
            for j in range(4):
                btn = self.buttons[i][j]
                btn.config(text="❓", state=tk.NORMAL, bg="lightgray")

    def reveal_symbol(self, i, j):
        if self.locked:
            return

        btn = self.buttons[i][j]
        index = i * 4 + j
        symbol = self.board[index]

        btn.config(text=symbol, bg="white")
        btn.update()

        if self.first_choice is None:
            self.first_choice = (i, j)
        elif self.second_choice is None and (i, j) != self.first_choice:
            self.second_choice = (i, j)
            self.root.after(500, self.check_match)

    def check_match(self):
        i1, j1 = self.first_choice
        i2, j2 = self.second_choice
        b1 = self.buttons[i1][j1]
        b2 = self.buttons[i2][j2]

        if self.board[i1 * 4 + j1] == self.board[i2 * 4 + j2]:
            b1.config(bg="lightgreen")
            b2.config(bg="lightgreen")
            b1.config(state=tk.DISABLED)
            b2.config(state=tk.DISABLED)
        else:
            b1.config(text="❓", bg="lightgray")
            b2.config(text="❓", bg="lightgray")

        self.first_choice = None
        self.second_choice = None

        if self.check_win():
            messagebox.showinfo("🎉 Congratulations", "You matched all the pairs!")

    def check_win(self):
        for row in self.buttons:
            for btn in row:
                if btn["state"] != tk.DISABLED:
                    return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
