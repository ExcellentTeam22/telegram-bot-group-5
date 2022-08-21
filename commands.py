import math


def factorial(number: str) -> str:
    return str(math.factorial(int(number)))


def palindrome(number: str) -> str:
    return "number is palindrom" if number == number[::-1] else "number is not palindrom"


def is_prime(n: str) -> str:
    for i in range(2, int(n)):
        if (int(n) % i) == 0:
            return "number is not prime"
    return "number is prime"


COMMANDS = {"/prime": is_prime, "/factorial": factorial, "/sqrt": "sqrtFunction", "/palindrom": palindrome}
