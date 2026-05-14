'''
user_high = float(input("Your high score: "))
user_weight = float(input("Your weight: "))
user_BMI = user_weight / (user_high ** 2)
if user_BMI <18.5:
    print("Underweight")
elif 18.5 <= user_BMI < 25:
    print("Normal weight")
elif 25 <= user_BMI < 30:
    print("Overweight")
else:
    print("Obese")
'''
'''
import random

print("欢迎来到猜数字游戏！")

while True:
    secret_number = random.randint(1, 100)
    max_attempts = 7
    attempts = 0

    print("\n我已经想好了一个 1 到 100 之间的数字。")
    print(f"你有 {max_attempts} 次机会来猜它。")

    while attempts < max_attempts:
        guess_input = input("\n请输入你猜的数字：")

        if not guess_input.isdigit():
            print("请输入有效的正整数。")
            continue

        guess = int(guess_input)
        attempts += 1

        if guess < 1 or guess > 100:
            print("数字范围应该在 1 到 100 之间。")
        elif guess < secret_number:
            print("猜小了！")
        elif guess > secret_number:
            print("猜大了！")
        else:
            print(f"恭喜你，猜对了！答案就是 {secret_number}。")
            print(f"你一共用了 {attempts} 次。")
            break
    else:
        print(f"\n很遗憾，次数用完了。正确答案是 {secret_number}。")

    play_again = input("\n还想再玩一次吗？输入 y 继续，其他键退出：")

    if play_again.lower() != "y":
        print("游戏结束，感谢游玩！")
        break
'''
'''
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i * j}", end="\t")
    print()
'''
'''
import utils as utils
print(utils.add(3, 5))
print(utils.is_prime(19))
print(utils.remove_spaces("hello world"))
'''
def celsius_to_fahrenheit(celsius):
    """摄氏度转华氏度"""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """华氏度转摄氏度"""
    return (fahrenheit - 32) * 5 / 9


while True:
    print("\n温度转换工具")
    print("1. 摄氏度 转 华氏度")
    print("2. 华氏度 转 摄氏度")
    print("3. 退出程序")

    choice = input("请选择功能：")

    if choice == "1":
        celsius = float(input("请输入摄氏度："))
        fahrenheit = celsius_to_fahrenheit(celsius)
        print(f"{celsius}℃ = {fahrenheit:.2f}℉")

    elif choice == "2":
        fahrenheit = float(input("请输入华氏度："))
        celsius = fahrenheit_to_celsius(fahrenheit)
        print(f"{fahrenheit}℉ = {celsius:.2f}℃")

    elif choice == "3":
        print("程序已退出。")
        break

    else:
        print("输入错误，请重新选择。")
