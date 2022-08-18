import math


def factorial(number: int) -> int:
    return math.factorial(number)


def palindrome(number) -> str:
    return number == number[::-1]


COMMANDS = {"/prime": "PrimeFunction", "/factorial": factorial, "/sqrt": "sqrtFunction", "/palindrom": palindrome}
