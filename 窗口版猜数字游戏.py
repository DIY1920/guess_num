import random
import tkinter as tk
from tkinter import messagebox


class GuessGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("猜数字游戏")
        self.root.geometry("420x240")
        self.root.resizable(False, False)

        self.secret = ""
        self.attempts = 0

        # 标题
        title_label = tk.Label(root, text="4位不重复数字猜谜游戏", font=("Arial", 16, "bold"))
        title_label.pack(pady=(20, 10))

        # 说明
        rule_label = tk.Label(
            root,
            text="规则：输入4位数字，系统会告诉你有几个位置正确\n数字不能重复，首位不能为0",
            font=("Arial", 10),
            justify="center"
        )
        rule_label.pack(pady=(0, 10))

        # 输入框
        self.entry = tk.Entry(root, width=20, font=("Arial", 16), justify="center")
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.check_guess())

        # 按钮
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        submit_btn = tk.Button(btn_frame, text="猜一下", command=self.check_guess, width=12, height=2)
        submit_btn.grid(row=0, column=0, padx=10)
        submit_btn.bind("<Return>", lambda event: self.check_guess())

        restart_btn = tk.Button(btn_frame, text="重新开始", command=self.start_new_game, width=12, height=2)
        restart_btn.grid(row=0, column=1, padx=10)

        # 结果显示
        self.result_var = tk.StringVar()
        self.result_var.set("游戏已开始")
        result_label = tk.Label(root, textvariable=self.result_var, font=("Arial", 11), fg="darkblue")
        result_label.pack(pady=10)

        self.start_new_game()

    def generate_secret(self):
        digits = list("123456789")
        first = random.choice(digits)
        rest = random.sample([d for d in "0123456789" if d != first], 3)
        return first + "".join(rest)

    def start_new_game(self):
        self.secret = self.generate_secret()
        self.attempts = 0
        self.result_var.set("新游戏开始！请输入4位数字，并按 Enter 猜一下")
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def check_guess(self):
        guess = self.entry.get().strip()

        if len(guess) != 4 or not guess.isdigit():
            self.result_var.set("请输入4位数字！")
            return

        # 用户输入允许重复数字；只要求是4位数字
        # 计算正确位置数
        count = sum(1 for i in range(4) if guess[i] == self.secret[i])
        self.attempts += 1

        if count == 4:
            self.result_var.set(f"恭喜！你在 {self.attempts} 次后猜中了！")
            messagebox.showinfo("胜利", f"答案是：{self.secret}\n你一共用了 {self.attempts} 次。")
            self.start_new_game()
        else:
            self.result_var.set(f"结果：{count} 个位置正确，已尝试 {self.attempts} 次")


if __name__ == "__main__":
    root = tk.Tk()
    app = GuessGameGUI(root)
    root.mainloop()