import random
import tkinter as tk
import tkinter.font as tk_font
from tkinter import messagebox

# 这个程序是一款“猜数字”游戏的图形界面版。
# 它使用 Tkinter 来创建窗口，让玩家在界面中输入数字，并实时看到猜测结果。
# 通过学习这段代码，我们可以理解：窗口创建、控件布局、事件绑定和状态更新。


class GuessGameGUI:
    def __init__(self, root):
        # root 表示主窗口对象。也就是说，整个程序的界面都挂在这个窗口上。
        self.root = root
        self.root.title("猜数字游戏")
        self.root.geometry("620x320")
        self.root.resizable(False, False)

        # 这里设置了界面中常用的字体样式，让中文文字显示得更自然、更统一。
        self.default_font = tk_font.Font(family="Microsoft YaHei", size=10)
        self.title_font = tk_font.Font(family="Microsoft YaHei", size=16, weight="bold")
        self.input_font = tk_font.Font(family="Microsoft YaHei", size=16)
        self.result_font = tk_font.Font(family="Microsoft YaHei", size=11)
        self.history_font = tk_font.Font(family="Microsoft YaHei", size=10)

        # 给 Tkinter 的所有基础控件设置默认字体，避免不同控件的字体风格不一致。
        self.root.option_add("*Font", self.default_font)
        self.root.option_add("*Button*Font", self.default_font)
        self.root.option_add("*Label*Font", self.default_font)
        self.root.option_add("*Entry*Font", self.default_font)

        # 这些变量用于保存当前游戏状态：秘密数字、已猜次数、历史记录。
        # 其中 secret 是答案，attempts 记录玩家尝试了多少次，history 保存每次结果。
        self.secret = ""
        self.attempts = 0
        self.history = []

        # 布局思路：把窗口分成左右两部分。
        # 左侧负责输入和操作，右侧负责显示提示和历史记录。
        main_frame = tk.Frame(root, padx=18, pady=18)
        main_frame.pack(fill="both", expand=True)

        left_panel = tk.Frame(main_frame, padx=10, pady=10)
        left_panel.pack(side="left", fill="y")

        right_panel = tk.Frame(main_frame, padx=10, pady=10)
        right_panel.pack(side="right", fill="both", expand=True)

        # 左侧上方展示游戏标题和规则说明，帮助玩家快速了解玩法。
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

        # 输入框用于让玩家输入猜测值；绑定回车键，可以直接提交，不用点按钮。
        self.entry = tk.Entry(left_panel, width=18, font=self.input_font, justify="center")
        self.entry.pack(pady=8)
        self.entry.bind("<Return>", lambda event: self.check_guess())

        # 这里放两个按钮：一个用于提交猜测，一个用于重新开始新一局。
        btn_frame = tk.Frame(left_panel)
        btn_frame.pack(pady=10)

        submit_btn = tk.Button(btn_frame, text="猜一下", command=self.check_guess, width=10, height=2)
        submit_btn.grid(row=0, column=0, padx=8)
        submit_btn.bind("<Return>", lambda event: self.check_guess())

        restart_btn = tk.Button(btn_frame, text="重新开始", command=self.start_new_game, width=10, height=2)
        restart_btn.grid(row=0, column=1, padx=8)

        # 右侧区域用于展示本次猜测的结果，以及所有历史记录。
        self.result_var = tk.StringVar()
        self.result_var.set("游戏已开始")
        self.result_label = tk.Label(
            right_panel,
            textvariable=self.result_var,
            font=self.result_font,
            fg="darkblue",
            justify="center",
            wraplength=300,
        )
        self.result_label.pack(anchor="w", pady=(0, 10), padx=5 )

        history_title = tk.Label(right_panel, text="历史记录", font=self.default_font, anchor="w")
        history_title.pack(anchor="w")

        self.history_text = tk.Text(right_panel, height=10, width=28, font=self.history_font)
        self.history_text.config(state="disabled")
        self.history_text.pack(fill="both", expand=True)

        # 程序启动时，自动初始化一局新游戏，让界面立即进入可操作状态。
        self.start_new_game()

    def generate_secret(self):
        # 这一步用于生成“答案”——一个 4 位不重复的随机数字。
        # 规则是：首位不能为 0，而且四个数字必须各不相同。
        digits = list("123456789")
        first = random.choice(digits)
        rest = random.sample([d for d in "0123456789" if d != first], 3)
        return first + "".join(rest)

    def start_new_game(self):
        # 重新开始一局游戏时，必须重置答案、次数和历史记录。
        self.secret = self.generate_secret()
        self.attempts = 0
        self.history = []
        self.entry.config(state="normal")
        self.result_var.set("新游戏开始！\n 请输入4位数字，看你最少能用几次猜出答案")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.refresh_history()
        self.root.update_idletasks()

    def refresh_history(self):
        # 这个方法会把历史记录显示到文本框中。
        # 这里使用了倒序输出，所以最新的猜测会出现在最上面，阅读体验更自然。
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        for item in reversed(self.history):
            self.history_text.insert(tk.END, item + "\n")
        self.history_text.config(state="disabled")

    def check_guess(self):
        # 先读取用户输入，并去掉前后空白字符。
        guess = self.entry.get().strip()

        # 玩家输入必须是 4 位纯数字，否则视为无效输入。
        # 这样可以避免出现字母、符号或长度不符合要求的情况。
        if len(guess) != 4 or not guess.isdigit():
            self.result_var.set("请输入4位数字！")
            self.result_label.config(fg="orange")
            return

        # 关键逻辑：统计玩家猜测中，有多少位数字和答案对应位置完全一致。
        # 例如：答案 1234，猜测 2244，那么只有第 2 位和第 3 位可能相同；
        # 这里返回的是“位置正确”的个数，不是数字出现次数。
        count = sum(1 for i in range(4) if guess[i] == self.secret[i])
        self.attempts += 1
        self.history.append(f"第 {self.attempts} 次：{guess} -> {count} 位正确")
        self.refresh_history()

        # 每次猜完后，清空输入框，让玩家继续下一轮猜测。
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

        # 如果 count == 4，说明四个位置都对，说明玩家猜中了答案。
        # 此时我们更新提示信息，并锁定输入框，避免继续提交。
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
    # 程序入口：创建窗口对象，并启动 Tkinter 的消息循环。
    # 也就是让窗口一直显示，直到用户关闭程序。
    root = tk.Tk()
    app = GuessGameGUI(root)
    root.mainloop()