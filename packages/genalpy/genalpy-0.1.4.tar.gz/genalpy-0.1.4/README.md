# Genetic algorithms with genalpy
Genalpy is an easy-to-use Python library to solve different types of optimization problems using genetic algorithms. 

### Installation
```
pip install genalpy
```

### Get started
How to find the extremum of a function:

```Python
from genalpy import Solver

# Instantiate a Multiplication object
extremum_solver = Solver(function='-x*x + 4', goal='max', dimensions=2, boundaries=[-100, 100])

# Call the solve method
result = extremum_solver.solve()
```
