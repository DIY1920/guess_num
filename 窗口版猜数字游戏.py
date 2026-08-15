import random
import tkinter as tk
import tkinter.font as tk_font
from tkinter import messagebox


class GuessGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("猜数字游戏")
        self.root.geometry("620x320")
        self.root.resizable(False, False)

        self.default_font = tk_font.Font(family="Microsoft YaHei", size=10)
        self.title_font = tk_font.Font(family="Microsoft YaHei", size=16, weight="bold")
        self.input_font = tk_font.Font(family="Microsoft YaHei", size=16)
        self.result_font = tk_font.Font(family="Microsoft YaHei", size=11)
        self.history_font = tk_font.Font(family="Microsoft YaHei", size=10)

        self.root.option_add("*Font", self.default_font)
        self.root.option_add("*Button*Font", self.default_font)
        self.root.option_add("*Label*Font", self.default_font)
        self.root.option_add("*Entry*Font", self.default_font)

        self.secret = ""
        self.attempts = 0
        self.history = []

        main_frame = tk.Frame(root, padx=18, pady=18)
        main_frame.pack(fill="both", expand=True)

        left_panel = tk.Frame(main_frame, padx=10, pady=10)
        left_panel.pack(side="left", fill="y")

        right_panel = tk.Frame(main_frame, padx=10, pady=10)
        right_panel.pack(side="right", fill="both", expand=True)

        title_label = tk.Label(left_panel, text="4位不重复数字猜谜游戏", font=self.title_font)
        title_label.pack(pady=(0, 10))

        rule_label = tk.Label(
            left_panel,
            text="规则：输入4位数字，系统会告诉你有几个位置正确\n允许重复数字，首位不能为0",
            font=self.default_font,
            justify="center",
            wraplength=240,
        )
        rule_label.pack(pady=(0, 10))

        self.entry = tk.Entry(left_panel, width=18, font=self.input_font, justify="center")
        self.entry.pack(pady=8)
        self.entry.bind("<Return>", lambda event: self.check_guess())

        btn_frame = tk.Frame(left_panel)
        btn_frame.pack(pady=10)

        submit_btn = tk.Button(btn_frame, text="猜一下", command=self.check_guess, width=10, height=2)
        submit_btn.grid(row=0, column=0, padx=8)
        submit_btn.bind("<Return>", lambda event: self.check_guess())

        restart_btn = tk.Button(btn_frame, text="重新开始", command=self.start_new_game, width=10, height=2)
        restart_btn.grid(row=0, column=1, padx=8)

        self.result_var = tk.StringVar()
        self.result_var.set("游戏已开始")
        self.result_label = tk.Label(
            right_panel,
            textvariable=self.result_var,
            font=self.result_font,
            fg="darkblue",
            justify="left",
            wraplength=260,
        )
        self.result_label.pack(anchor="w", pady=(0, 10))

        history_title = tk.Label(right_panel, text="历史记录", font=self.default_font, anchor="w")
        history_title.pack(anchor="w")

        self.history_text = tk.Text(right_panel, height=10, width=28, font=self.history_font)
        self.history_text.config(state="disabled")
        self.history_text.pack(fill="both", expand=True)

        self.start_new_game()

    def generate_secret(self):
        digits = list("123456789")
        first = random.choice(digits)
        rest = random.sample([d for d in "0123456789" if d != first], 3)
        return first + "".join(rest)

    def start_new_game(self):
        self.secret = self.generate_secret()
        self.attempts = 0
        self.history = []
        self.entry.config(state="normal")
        self.result_var.set("新游戏开始！请输入4位数字，并按 Enter 猜一下")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.refresh_history()
        self.root.update_idletasks()

    def refresh_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        for item in self.history:
            self.history_text.insert(tk.END, item + "\n")
        self.history_text.config(state="disabled")

    def check_guess(self):
        guess = self.entry.get().strip()

        if len(guess) != 4 or not guess.isdigit():
            self.result_var.set("请输入4位数字！")
            self.result_label.config(fg="orange")
            return

        count = sum(1 for i in range(4) if guess[i] == self.secret[i])
        self.attempts += 1
        self.history.append(f"第 {self.attempts} 次：{guess} -> {count} 位正确")
        self.refresh_history()

        if count == 4:
            result_text = f"恭喜！你在 {self.attempts} 次后猜中了！\n最终结果：{count} 个位置正确"
            self.result_var.set(result_text)
            self.result_label.config(fg="green")
            self.root.update_idletasks()
            self.entry.config(state="disabled")
            self.root.after(1500, self.start_new_game)
        else:
            result_text = f"结果：{count} 个位置正确，已尝试 {self.attempts} 次"
            self.result_var.set(result_text)
            self.result_label.config(fg="red")
            self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = GuessGameGUI(root)
    root.mainloop()