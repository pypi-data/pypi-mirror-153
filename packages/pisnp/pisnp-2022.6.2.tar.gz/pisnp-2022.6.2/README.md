# PisNP

Version `2022.6.2`

P is NP? (Polynomial is Non-polynomial?)

## Installation

```shell
conda create -n pisnp python=3.10
conda activate pisnp
pip install pisnp
```

## Exact Cover

Solve a general exact cover problem:

```python
from pisnp.exact_cover import ExactCoverSolver

solver = ExactCoverSolver(
    universe={1, 2, 3, 4, 5, 6, 7},
    subsets={
        'A': [1, 4, 7],
        'B': [1, 4],
        'C': [4, 5, 7],
        'D': [3, 5, 6],
        'E': [2, 3, 6, 7],
        'F': [2, 7],
        'G': [1, 4, 5],
    },
)

for solution in solver.solve():
    print(solution)
    solver.display(solution=solution)
    print()
```

Solve a sudoku problem:

```python
from pisnp.exact_cover import SudokuSolver

solver = SudokuSolver(board=[
    [6, 0, 0, 1, 0, 0, 0, 0, 8],
    [0, 0, 0, 8, 0, 0, 2, 0, 0],
    [0, 3, 8, 0, 5, 0, 1, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 9, 2],
    [0, 0, 4, 3, 0, 8, 6, 0, 0],
    [3, 7, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 7, 0, 5, 2, 6],
    [0, 0, 2, 0, 0, 4, 0, 0, 0],
    [9, 0, 7, 0, 0, 6, 0, 0, 1]
])

solutions = list(solver.solve())
print(f'number of solutions: {len(solutions)}')
for solution in solutions:
    solver.display(solution=solution)
    print()
```

## Traveling Salesman

Solve a traveling salesman problem:

```pycon
from pisnp.traveling_salesman import (
    BacktrackTravelingSalesmanSolver,
    TravelingSalesmanGenerator,
)

_, costs = TravelingSalesmanGenerator.generate(
    num_cities=10,
    method=TravelingSalesmanGenerator.Method.random,
)
solver = BacktrackTravelingSalesmanSolver(costs=costs)
min_cost, min_path = timed_solve(s=solver)
solver.display()
```

## Unit Test

Run testcases in all files:

```shell
PYTHONPATH='src' python -m unittest discover -s tests
```

Run testcases in one file:

```shell
python -m unittest tests/test_exact_cover_solver.py
```
