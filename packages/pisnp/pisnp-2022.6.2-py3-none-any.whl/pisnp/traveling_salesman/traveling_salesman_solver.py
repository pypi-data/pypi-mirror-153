# coding=utf-8
#
# traveling_salesman_solver.py in pisnp/traveling_salesman
#
# created by 谢方圆 (XIE Fangyuan) on 2022-06-06
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Solver for traveling salesman problem.


from abc import ABCMeta, abstractmethod
from functools import reduce
from itertools import pairwise, permutations

from sty import fg

from pisnp.solver import Solver


class TravelingSalesmanSolver(Solver, metaclass=ABCMeta):
    def __init__(self, costs: list[list[float]]):
        self.costs, self.n = costs, len(costs)
        self.min_cost, self.min_path = float('inf'), []

    @abstractmethod
    def solve(self) -> tuple[int | float, list[int]]:
        pass

    def display(self) -> None:
        if not isinstance(self.costs[0][0], int):
            print(f'min_cost={self.min_cost}\nmin_path={self.min_path}')
            return

        costs = [list(map(lambda c: f'{c:>3d}', row)) for row in self.costs]
        for c1, c2 in pairwise(self.min_path):
            costs[c1][c2] = f'{fg.green}{costs[c1][c2]}{fg.rs}'
        print(f'     {" ".join(map(lambda i: f"c{i:<2d}", range(self.n)))}')
        for r, row in enumerate(costs):
            print(f'r{r:<2d}  {" ".join(row)}')
        print(f'min_cost={self.min_cost}\nmin_path={self.min_path}')


class BruteForceTravelingSalesmanSolver(TravelingSalesmanSolver):
    def __init__(self, costs: list[list[float]]):
        super().__init__(costs)

    def solve(self) -> tuple[int | float, list[int]]:
        for path in map(
                lambda permutation: [0] + list(permutation) + [0],
                permutations(range(1, self.n))
        ):
            cost = reduce(
                lambda c, e: c + self.costs[e[0]][e[1]],
                pairwise(path), 0,
            )
            if cost < self.min_cost:
                self.min_cost, self.min_path = cost, path
        return self.min_cost, self.min_path


class BacktrackTravelingSalesmanSolver(TravelingSalesmanSolver):
    def __init__(self, costs: list[list[float]]):
        super().__init__(costs)
        self.cost, self.next_cities = 0, [-1] * self.n

    def solve(self) -> tuple[int | float, list[int]]:
        self.__backtrack(visiting=0, num_visited=0)
        return self.min_cost, self.min_path

    def __backtrack(self, visiting: int, num_visited: int) -> None:
        if self.cost > self.min_cost: return
        if num_visited == self.n:
            self.min_cost, self.min_path = self.cost, [0]
            while next_city := self.next_cities[self.min_path[-1]]:
                self.min_path.append(next_city)
            self.min_path.append(0)
        else:
            for city in range(self.n):
                if (city == visiting or self.next_cities[city] != -1) and \
                        (num_visited != self.n - 1 or city != 0): continue
                self.cost += self.costs[visiting][city]
                self.next_cities[visiting] = city
                self.__backtrack(visiting=city, num_visited=num_visited + 1)
                self.next_cities[visiting] = -1
                self.cost -= self.costs[visiting][city]
