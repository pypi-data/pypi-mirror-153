# coding=utf-8
#
# solver.py in pisnp
#
# created by 谢方圆 (XIE Fangyuan) on 2022-06-05
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Abstract base problem solver.


from abc import ABCMeta, abstractmethod
from typing import Any


class Solver(metaclass=ABCMeta):
    @abstractmethod
    def solve(self) -> Any:
        """Override this function to solve a specific problem.

        Returns:
            The solution.
        """
        pass

    def display(self, *args, **kwargs) -> None:
        pass
