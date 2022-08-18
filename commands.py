import math


def factorial(number: int) -> int:
    return math.factorial(number)


def palindrome(number) -> str:
    return number == number[::-1]


def is_prime(n: int) -> bool:
    for i in range(2, n):
        if (n % i) == 0:
            return False
    return True


COMMANDS = {"/prime": is_prime, "/factorial": factorial, "/sqrt": "sqrtFunction", "/palindrom": palindrome}
