# coding=utf-8
#
# draft.py in pisnp
#
# created by 谢方圆 (XIE Fangyuan) on 2022-06-05
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Draft.



from collections import OrderedDict


def main() -> None:
    a = OrderedDict({1: 1, 2: 2, 3: 2})
    a[0] = 1
    a[-1] = 9
    print(a)


if __name__ == '__main__':
    main()
