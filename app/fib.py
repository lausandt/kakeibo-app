from typing import Generator


def _fib(n: int) -> Generator:
    a, b = 0, 1
    stop = 0
    while stop <= n:
        yield a
        a, b = b, a + b
        stop += 1


def fib(n: int) -> int:
    if n < 0:
        raise ValueError("you can`t have a negative element of a sequence")
    if n < 2:
        return n
    return list(_fib(n)).pop()
