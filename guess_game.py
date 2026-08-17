import random

# 控制台版猜数字游戏：系统生成一个 4 位不重复数字，玩家不断提交猜测。

def main():
    # 生成4位不重复数字（首位不能为0，且每一位都不同）
    digits = list('123456789')
    first = random.choice(digits)
    rest = random.sample([d for d in '0123456789' if d != first], 3)
    secret = first + ''.join(rest)

    # 展示游戏规则和说明信息
    print("="*40)
    print("✅ 4位不重复数字已生成！")
    print("规则：数字和位置都正确才计数")
    print("例如：秘密数字1234，猜2244 → 返回2")
    print("="*40)

    attempts = 0
    while True:
        # 读取用户输入；空字符串表示退出当前游戏
        guess = input("\n🔍 请输入你的猜测（直接回车退出）：").strip()
        if not guess:
            print(f"游戏结束！答案是：{secret}")
            return

        # 只接受 4 位数字，避免无效输入导致判断错误
        if len(guess) != 4 or not guess.isdigit():
            print("⚠️ 请输入4位数字！")
            continue

        # 统计“位置正确”的数字个数
        count = sum(1 for i in range(4) if guess[i] == secret[i])

        print(f"→ 结果：{count}个正确")
        attempts += 1

        # 猜中后结束游戏，给出总尝试次数
        if count == 4:
            print(f"🎉 恭喜！你用{attempts}次猜中了！")
            break

if __name__ == "__main__":
    main()
