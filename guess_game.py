import random

def main():
    # 生成4位不重复数字（首位非0）
    digits = list('123456789')
    first = random.choice(digits)
    rest = random.sample([d for d in '0123456789' if d != first], 3)
    secret = first + ''.join(rest)
    
    print("="*40)
    print("✅ 4位不重复数字已生成！")
    print("规则：数字和位置都正确才计数")
    print("例如：秘密数字1234，猜2244 → 返回2")
    print("="*40)
    
    attempts = 0
    while True:
        guess = input("\n🔍 请输入你的猜测（直接回车退出）：").strip()
        if not guess: 
            print(f"游戏结束！答案是：{secret}")
            return
            
        if len(guess) != 4 or not guess.isdigit():
            print("⚠️ 请输入4位数字！")
            continue
            
        # 计算正确位置数
        count = sum(1 for i in range(4) if guess[i] == secret[i])
        
        print(f"→ 结果：{count}个正确")
        attempts += 1
        
        if count == 4:
            print(f"🎉 恭喜！你用{attempts}次猜中了！")
            break

if __name__ == "__main__":
    main()
