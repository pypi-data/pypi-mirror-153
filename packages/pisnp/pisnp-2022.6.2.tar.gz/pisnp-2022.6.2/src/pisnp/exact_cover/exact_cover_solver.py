# coding=utf-8
#
# exact_cover_solver.py in pisnp/exact_cover
#
# created by 谢方圆 (self.universeIE Fangyuan) on 2022-06-05
# Copyright © 2022 谢方圆 (self.universeIE Fangyuan). All rights reserved.
#
# Solver for exact cover problem.


from string import ascii_lowercase, ascii_uppercase, digits
from typing import Any, Generator, Sequence

from sty import fg

from pisnp.solver import Solver


class ExactCoverSolver(Solver):
    def __init__(self, universe: set, subsets: dict[Any, Sequence]):
        """Solver for an exact cover problem.

        Args:
            universe: A universe.
            subsets: A collection of named subsets of the universe.
        """
        self.universe_o, self.subsets, self.solution = universe, subsets, []
        # Transform the universe.
        self.universe: dict[Any, set] = {x: set() for x in universe}
        for name, subset in self.subsets.items():
            for value in subset:
                self.universe[value].add(name)

    def solve(self) -> Generator:
        """Solve an exact cover problem by algorithm x.

        Returns:
            A list of disjoint subsets whose union is the universe.
        """
        if not self.universe:
            # If no column, a solution is found.
            yield self.solution.copy()
        else:
            # Choose the column with minimum length to search quicker.
            # If min len(self.universe[x]) == 0, there is no solution.
            col = min(self.universe, key=lambda x: len(self.universe[x]))
            for row in list(self.universe[col]):
                # Select one row.
                self.solution.append(row)

                # Delete rows and columns.
                cols = []
                for c in self.subsets[row]:
                    for r in self.universe[c]:
                        # Delete a row in universe.
                        for k in self.subsets[r]:
                            if k != c:
                                self.universe[k].remove(r)
                    # Delete a column in universe and save it for restore.
                    cols.append(self.universe.pop(c))

                # Backtrack to choose more rows.
                for s in self.solve():
                    yield s

                # Restore universe.
                for c in reversed(self.subsets[row]):
                    self.universe[c] = cols.pop()
                    for r in self.universe[c]:
                        for k in self.subsets[r]:
                            if k != c:
                                self.universe[k].add(r)

                # Deselect one row.
                self.solution.pop()

    def display(self, solution: Sequence | None = None) -> None:
        print(f'   {" ".join(map(str, cols := sorted(self.universe_o)))}')
        for i, subset in self.subsets.items():
            print(
                f'''{fg.green if solution and i in solution else ''}{i}: {
                " ".join("@" if c in subset else "." for c in cols)}{
                fg.rs if solution and i in solution else ''}'''
            )


class SudokuSolver(ExactCoverSolver):
    def __init__(self, board: Sequence[Sequence[int]]):
        self.n = len(board)
        assert self.n == len(board[0]), f'board must be a square.'
        self.m = int(self.n ** 0.5)
        assert self.m ** 2 == self.n, f'board length must be a square number.'

        self.board = board

        # Initialize the universe and subsets for sudo.
        universe = set(
            [f'cell[{r},{c}]' for r in range(self.n) for c in range(self.n)] +
            [f'row[{r}]has{v}' for r in range(self.n)
             for v in range(1, self.n + 1)] +
            [f'col[{c}]has{v}' for c in range(self.n)
             for v in range(1, self.n + 1)] +
            [f'grid[{r},{c}]has{v}' for r in range(self.m)
             for c in range(self.m) for v in range(1, self.n + 1)]
        )
        subsets: dict[int, list[str]] = {
            v - 1 + c * self.n + r * self.n ** 2: [
                f'cell[{r},{c}]', f'row[{r}]has{v}', f'col[{c}]has{v}',
                f'grid[{r // self.m},{c // self.m}]has{v}']
            for r in range(self.n)
            for c in range(self.n) for v in range(1, self.n + 1)
        }

        super(SudokuSolver, self).__init__(universe=universe, subsets=subsets)

        # Remove rows and columns according to the given board.
        for r, row in enumerate(self.board):
            for c, v in enumerate(row):
                if v == 0: continue
                for cc in [f'cell[{r},{c}]', f'row[{r}]has{v}',
                           f'col[{c}]has{v}',
                           f'grid[{r // self.m},{c // self.m}]has{v}']:
                    for rr in self.universe[cc]:
                        for k in self.subsets[rr]:
                            if k != cc:
                                self.universe[k].remove(rr)
                    self.universe.pop(cc)

    def display(self, solution: Sequence | None = None) -> None:
        # Copy the original board.
        board = [list(row) for row in self.board]

        # Fill the board with solution.
        for i in solution:
            board[i // self.n ** 2][i // self.n % self.n] = i % self.n + 1

        # Print the board.
        def expand_line(line):
            return line[0] + line[5:9].join(
                [line[1:5] * (self.m - 1)] * self.m) + line[9:13]

        line0 = expand_line('╔═══╤═══╦═══╗')
        line1 = expand_line('║ . │ . ║ . ║')
        line2 = expand_line('╟───┼───╫───╢')
        line3 = expand_line('╠═══╪═══╬═══╣')
        line4 = expand_line('╚═══╧═══╩═══╝')
        symbol = ' ' + digits + ascii_lowercase + ascii_uppercase
        nums = [[''] + [
            symbol[v] if self.board[r][c] else f'{fg.green}{symbol[v]}{fg.rs}'
            for c, v in enumerate(row)] for r, row in enumerate(board)]
        print(line0)
        for r in range(1, self.n + 1):
            print(''.join(
                n + s for n, s in zip(nums[r - 1], line1.split('.'))
            ))
            print([line2, line3, line4][(r % self.n == 0) + (r % self.m == 0)])
