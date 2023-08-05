def hello():
    print('Hello world!')


def bye():
    print('Bye!')


def fib_2(n):
    if n <= 2:
        return 1
    return fib_2(n-1) + fib_2(n-2)