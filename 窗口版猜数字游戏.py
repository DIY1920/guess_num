import random
import tkinter as tk
import tkinter.font as tk_font
from tkinter import messagebox

# GUI 版猜数字游戏：通过 Tkinter 创建窗口界面，用户在窗口中输入数字进行猜测。


class GuessGameGUI:
    def __init__(self, root):
        # 保存主窗口对象，并设置窗口标题与大小
        self.root = root
        self.root.title("猜数字游戏")
        self.root.geometry("620x320")
        self.root.resizable(False, False)

        # 设置界面常用字体，方便中文显示
        self.default_font = tk_font.Font(family="Microsoft YaHei", size=10)
        self.title_font = tk_font.Font(family="Microsoft YaHei", size=16, weight="bold")
        self.input_font = tk_font.Font(family="Microsoft YaHei", size=16)
        self.result_font = tk_font.Font(family="Microsoft YaHei", size=11)
        self.history_font = tk_font.Font(family="Microsoft YaHei", size=10)

        # 设置全局默认字体，保证控件风格统一
        self.root.option_add("*Font", self.default_font)
        self.root.option_add("*Button*Font", self.default_font)
        self.root.option_add("*Label*Font", self.default_font)
        self.root.option_add("*Entry*Font", self.default_font)

        # 保存当前秘密数字、猜测次数和历史记录
        self.secret = ""
        self.attempts = 0
        self.history = []

        # 主布局：左右两栏，左侧输入区，右侧结果区
        main_frame = tk.Frame(root, padx=18, pady=18)
        main_frame.pack(fill="both", expand=True)

        left_panel = tk.Frame(main_frame, padx=10, pady=10)
        left_panel.pack(side="left", fill="y")

        right_panel = tk.Frame(main_frame, padx=10, pady=10)
        right_panel.pack(side="right", fill="both", expand=True)

        # 左上方标题和规则说明
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

        # 用户输入框，按回车即可提交答案
        self.entry = tk.Entry(left_panel, width=18, font=self.input_font, justify="center")
        self.entry.pack(pady=8)
        self.entry.bind("<Return>", lambda event: self.check_guess())

        # 按钮区域：猜一下 和 重新开始
        btn_frame = tk.Frame(left_panel)
        btn_frame.pack(pady=10)

        submit_btn = tk.Button(btn_frame, text="猜一下", command=self.check_guess, width=10, height=2)
        submit_btn.grid(row=0, column=0, padx=8)
        submit_btn.bind("<Return>", lambda event: self.check_guess())

        restart_btn = tk.Button(btn_frame, text="重新开始", command=self.start_new_game, width=10, height=2)
        restart_btn.grid(row=0, column=1, padx=8)

        # 结果显示区和历史记录区
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

        # 界面初始化时立即生成新游戏
        self.start_new_game()

    def generate_secret(self):
        # 生成随机的 4 位不重复数字：首位不能为 0，且后面从剩余数字中抽取 3 位
        digits = list("123456789")
        first = random.choice(digits)
        rest = random.sample([d for d in "0123456789" if d != first], 3)
        return first + "".join(rest)

    def start_new_game(self):
        # 重新开始一局，重置秘密数字、次数和历史记录
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
        # 更新历史记录框，按时间倒序显示每次猜测结果
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        for item in reversed(self.history):
            self.history_text.insert(tk.END, item + "\n")
        self.history_text.config(state="disabled")

    def check_guess(self):
        # 获取输入并过滤空白字符
        guess = self.entry.get().strip()

        # 只有 4 位纯数字才算有效输入
        if len(guess) != 4 or not guess.isdigit():
            self.result_var.set("请输入4位数字！")
            self.result_label.config(fg="orange")
            return

        # 统计“位置正确”的个数，例：1234 与 2244 → 2
        count = sum(1 for i in range(4) if guess[i] == self.secret[i])
        self.attempts += 1
        self.history.append(f"第 {self.attempts} 次：{guess} -> {count} 位正确")
        self.refresh_history()

        # 清空输入框，让玩家继续下一轮猜测
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

        # 猜中后更新结果并锁定输入框，避免继续输入
        if count == 4:
            result_text = f"恭喜！你在 {self.attempts} 次后猜中了！\n最终结果：{count} 个位置正确"
            self.result_var.set(result_text)
            self.result_label.config(fg="green")
            self.root.update_idletasks()
            self.entry.config(state="disabled")
        else:
            result_text = f"结果：{count} 个位置正确，已尝试 {self.attempts} 次"
            self.result_var.set(result_text)
            self.result_label.config(fg="red")
            self.root.update_idletasks()


if __name__ == "__main__":
    # 程序入口：启动窗口并进入消息循环
    root = tk.Tk()
    app = GuessGameGUI(root)
    root.mainloop()