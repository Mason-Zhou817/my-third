"""
个人工具函数库 personal_utils.py
封装常用的字符串处理、数学计算和列表处理函数。
"""


# ========== 字符串处理 ==========

def remove_spaces(text):
    """去除字符串中的所有空格"""
    return text.replace(" ", "")


def reverse_string (text):
    """反转字符串"""
    return text[::-1]


def count_words(text):
    """统计英文句子中的单词数量"""
    return len(text.split())


def is_palindrome(text):
    """判断字符串是否为回文"""
    text = text.replace(" ", "").lower()
    return text == text[::-1]


def capitalize_words(text):
    """将每个单词首字母大写"""
    return text.title()


# ========== 数学计算 ==========

def add(a, b):
    """加法"""
    return a + b


def subtract(a, b):
    """减法"""
    return a - b


def multiply(a, b):
    """乘法"""
    return a * b


def divide(a, b):
    """除法"""
    if b == 0:
        return "错误：除数不能为 0"
    return a / b


def factorial(n):
    """计算阶乘"""
    if n < 0:
        return "错误：负数没有阶乘"
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def is_prime(n):
    """判断是否为质数"""
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


def average(numbers):
    """计算平均值"""
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)


# ========== 列表处理 ==========

def find_max(numbers):
    """查找最大值"""
    if len(numbers) == 0:
        return None
    return max(numbers)


def find_min(numbers):
    """查找最小值"""
    if len(numbers) == 0:
        return None
    return min(numbers)


def remove_duplicates(items):
    """去除列表中的重复元素"""
    result = []

    for item in items:
        if item not in result:
            result.append(item)

    return result


def sort_numbers(numbers, reverse=False):
    """排序数字列表"""
    return sorted(numbers, reverse=reverse)


# ========== 测试代码 ==========

if __name__ == "__main__":
    print(remove_spaces("hello world python"))
    print(reverse_string("Python"))
    print(count_words("I love Python programming"))
    print(is_palindrome("level"))

    print(add(10, 5))
    print(divide(10, 2))
    print(factorial(5))
    print(is_prime(17))
    print(average([80, 90, 100]))

    print(find_max([3, 8, 2, 10]))
    print(remove_duplicates([1, 2, 2, 3, 4, 4]))
