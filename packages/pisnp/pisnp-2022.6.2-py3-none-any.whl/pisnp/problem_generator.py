# coding=utf-8
#
# problem_generator.py in pisnp
#
# created by 谢方圆 (XIE Fangyuan) on 2022-06-05
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Abstract base problem generator.


from abc import ABCMeta, abstractmethod
from typing import Any


class ProblemGenerator(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def generate(*args, **kwargs) -> Any:
        """Override this function to generate a specific problem.

        Returns:
            A problem.
        """
        pass
