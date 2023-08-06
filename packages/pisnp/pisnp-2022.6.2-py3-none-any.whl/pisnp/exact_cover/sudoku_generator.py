# coding=utf-8
#
# sudoku_generator.py in pisnp/exact_cover
#
# created by 谢方圆 (XIE Fangyuan) on 2022-06-05
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Generator for sudoku problem.


from random import sample

from pisnp.problem_generator import ProblemGenerator


class SudokuGenerator(ProblemGenerator):
    @staticmethod
    def generate(m: int, ratio: float = 0.2) -> list[list[int]]:
        """Generate a sudoku problem of size m^2 by m^2.

        Args:
            m: Square root of the size of the sudoku board.
            ratio: Ratio of empty cells.

        Returns:
            A m^2 by m^2 2d list representing a sudoku board.
        """
        n, m_range = m ** 2, range(m)
        rows = [g * m + r for g in sample(population=m_range, k=m)
                for r in sample(population=range(m), k=m)]
        cols = [g * m + c for g in sample(population=m_range, k=m)
                for c in sample(population=range(m), k=m)]
        nums = sample(population=range(1, n + 1), k=n)
        # Generate a solution.
        board = [[nums[(r % m * m + r // m + c) % n]
                  for c in cols] for r in rows]
        # Remove some numbers.
        for i in sample(population=range(n ** 2), k=int(n ** 2 * ratio)):
            board[i // n][i % n] = 0
        return board


if __name__ == '__main__':
    SudokuGenerator().generate(m=3)
