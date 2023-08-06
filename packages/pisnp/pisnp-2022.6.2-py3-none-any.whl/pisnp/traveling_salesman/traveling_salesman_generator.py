# coding=utf-8
#
# traveling_salesman_generator.py in pisnp/traveling_salesman
#
# created by 谢方圆 (XIE Fangyuan) on 2022-06-06
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Generator for traveling salesman problem.


from enum import Enum

import numpy as np

from pisnp.problem_generator import ProblemGenerator


class TravelingSalesmanGenerator(ProblemGenerator):
    class Method(Enum):
        """Method for generate a traveling salesman problem.
        """
        euclid = 'euclid'
        random = 'random'

    @classmethod
    def generate(
            cls,
            num_cities: int,
            dimension: int = 2,
            max_v: int = 50,
            method: Method = Method.euclid,
    ) -> tuple[list[list[int]] | None, list[list[int | float]]]:
        """Generate a traveling salesman problem.

        Args:
            num_cities: Number of cities.
            dimension: Dimension of city coordinates.
            max_v: Max value of each dimension of the city coordinates.
            method: Method for generate a traveling salesman problem.

        Returns:
            City coordinates, [num_cities, dimension] or None.
            Costs between every two cities, [num_cities, num_cities].
        """
        if method == cls.Method.euclid:
            return cls.__generate_euclid(
                num_cities=num_cities,
                dimension=dimension,
                max_v=max_v,
            )
        elif method == cls.Method.random:
            return None, cls.__generate_random(
                num_cities=num_cities,
                max_v=max_v,
            )
        else:
            assert False, f'{method} is an invalid generating method.'

    @staticmethod
    def __generate_euclid(
            num_cities: int,
            dimension: int = 2,
            max_v: int = 50,
    ) -> tuple[list[list[int]], list[list[float]]]:
        """Generate costs between every two cities given the number of cities.
        Here Euclid distances are used as the costs.

        Args:
            num_cities: Number of cities.
            dimension: Dimension of city coordinates.
            max_v: Max value of each dimension of the city coordinates.

        Returns: City coordinates, [num_cities, dimension].
            Costs between every two cities, [num_cities, num_cities].
        """
        cities = np.random.randint(max_v, size=(num_cities, dimension))
        idx1, idx2 = np.meshgrid(indices := np.arange(num_cities), indices)
        costs = (np.sum(a=(cities[idx1] - cities[idx2]) ** 2, axis=-1)) ** 0.5
        return [c.tolist() for c in cities], [c.tolist() for c in costs]

    @staticmethod
    def __generate_random(
            num_cities: int,
            max_v: int = 50,
    ) -> list[list[int]]:
        """Generate costs between every two cities given the number of cities.
        Costs are generated randomly.

        Args:
            num_cities: Number of cities.
            max_v: Max value of each dimension of the city coordinates.

        Returns:
            Costs between every two cities, [num_cities, num_cities].
        """
        return (np.random.randint(
            low=1, high=max_v, size=(num_cities, num_cities),
        ) * (1 - np.eye(N=num_cities, dtype=int))).tolist()


if __name__ == '__main__':
    print(TravelingSalesmanGenerator.generate(
        num_cities=4,
        method=TravelingSalesmanGenerator.Method.euclid)
    )
