# coding=utf-8
#
# draft.py in pisnp
#
# created by 谢方圆 (XIE Fangyuan) on 2022-06-05
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Draft.


from copy import deepcopy
from collections import OrderedDict


def main() -> None:
    a = [[[1, 2]], [[3, 4]]]

    b = a.copy()
    b[0][0][0] = 6
    print(a, b)
    print(id(a) == id(b))  # False
    print(id(a[0]) == id(b[0]))  # True
    print(id(a[0][0]) == id(b[0][0]))  # True
    print(id(a[0][0][0]) == id(b[0][0][0]))  # True

    b = list(a)
    b[0][0][0] = 5
    print(a, b)
    print(id(a) == id(b))  # False
    print(id(a[0]) == id(b[0]))  # True
    print(id(a[0][0]) == id(b[0][0]))  # True
    print(id(a[0][0][0]) == id(b[0][0][0]))  # True

    b = deepcopy(a)
    print(a, b)
    print(id(a) == id(b))  # False
    print(id(a[0]) == id(b[0]))  # False
    print(id(a[0][0]) == id(b[0][0]))  # False
    print(id(a[0][0][0]) == id(b[0][0][0]))  # True

    b[0][0][0] = 8
    print(a, b)
    print(id(a) == id(b))  # False
    print(id(a[0]) == id(b[0]))  # False
    print(id(a[0][0]) == id(b[0][0]))  # False
    print(id(a[0][0][0]) == id(b[0][0][0]))  # False


if __name__ == '__main__':
    main()
