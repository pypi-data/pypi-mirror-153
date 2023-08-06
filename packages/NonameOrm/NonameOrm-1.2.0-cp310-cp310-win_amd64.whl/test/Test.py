import sqlite3


class A:
    pass


class B(A):
    pass


class C(B):
    pass


def test(a: B):
    pass


c = A()

test(a=c)

if __name__ == '__main__':
    pass
