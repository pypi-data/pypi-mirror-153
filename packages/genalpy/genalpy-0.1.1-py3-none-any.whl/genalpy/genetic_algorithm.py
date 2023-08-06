import math
import numpy as np
from genalpy.utils import total_distance, stop_condition
from genalpy.population import Population

class Solver:
    """
    Instantiates a solving operator for optimization problems.
    Uses the selected methods of Genetic Algorithm.

    :param task_type: problem to solve, available - func_extremum, TSP
    :type task_type: string

    :param create_population_method: method of creating initial population, available -
        shotgun, focusing (additional parameter - focus_boundaries)
    :type create_population_method: string

    :param selection_method: method of parent selection, available - proportional, ranging, annealing
    :type selection_method: string

    :param recombination_method: method of recombination, available - discrete, transitional, linear
    :type recombination_method: string

    :param mutation_method: method of mutation, available - real_number
    :type mutation_method: string

    :param reduction_method: method of reduction, available - uniform_random_replacement, selective_scheme
    :type reduction_method: string

    :param stop_criterion: condition to stop the cycle, available - generations_limit, fitness_stability
    :type stop_criterion: string

    :param stop_criterion_value: implication depends on stop_criterion:
            - 'generations_limit' -> max number of generations
            - 'fitness_stability' -> max difference between the best fitness values in the last generations
    :type stop_criterion_value: int/float

    :param n_pop: number of elements in population, default - 1000
    :type n_pop: int

    In case of task_type=='func_extremum':

        :param function: represented as a string, examples:
            - 2dim: 'x**2 + x - 1'
            - 3dim: 'x*y - 2*(np.cos(y)+1)'
        :type function: string

        :param goal: max or min, default - min
        :type goal: string

        :param dimensions: number of dimensions (currently available 2 or 3), default - 3
        :type dimensions: int

        :param boundaries: min and max possible values of variable coordinates:
            - 2dim: [Xmin, Xmax]
            - 3dim: [Xmin, Xmax, Ymin, Ymax]
        :type boundaries: list of floats

        :param focus_boundaries: parameter for create_population_method=='focusing':
            - 2dim: [Xmin, Xmax]
            - 3dim: [Xmin, Xmax, Ymin, Ymax]
        :type focus_boundaries: list of floats

    In case of task_type=='TSP':

        :param points: cities to visit, the first city must be the starting
            and simultaneously the ending point of the route
        :type points: list of 2-element lists [float, float], X and Y coordinates respectively
    """
    def __init__(self, task_type='func_extremum', create_population_method='shotgun',
                 selection_method='ranging', recombination_method='transitional', mutation_method='real_number',
                 reduction_method='selective_scheme', stop_criterion='generations_limit', stop_value=20,
                 n_pop=50, function=None, goal='min', dimensions=3,
                 boundaries=None, focus_boundaries=None, points=None):
        try:
            self.task_type = task_type
            self.create_population_method = create_population_method
            self.selection_method = selection_method
            self.recombination_method = recombination_method
            self.mutation_method = mutation_method
            self.reduction_method = reduction_method
            self.stop_criterion = stop_criterion
            self.stop_value = stop_value
            self.n_pop = n_pop
            self.goal = goal
            self.dimensions = dimensions
            self.boundaries = boundaries
            self.focus_boundaries = focus_boundaries
            self.points = points
            # definition of the fitness_func
            if task_type == 'func_extremum':
                if self.dimensions == 2:
                    self.transitional_func = lambda x: eval(function)
                    self.fitness_func = lambda coords: self.transitional_func(coords[0])
                elif self.dimensions == 3:
                    self.transitional_func = lambda x, y: eval(function)
                    self.fitness_func = lambda coords: self.transitional_func(coords[0], coords[1])
                else:
                    print("Change the number of dimensions to the following: 2/3")
            elif task_type == 'TSP':
                self.fitness_func = lambda p: total_distance(p)
            else:
                print('There is no solution for your task... Try the following: func_extremum/TSP')
        except:
            print('Check the available parameters')

    def solve(self):
        """
        Solves the optimization problems based on parameters using Genetic Algorithm.

        :return: The optimum solution.
        :rtype: float
        """
        population = Population(self.task_type, self.n_pop, self.fitness_func, self.goal, self.dimensions,
                                self.boundaries, self.points)
        population.create(self.create_population_method, self.focus_boundaries)
        generation_num = 0
        accuracy = 1
        # temperature for simulated annealing
        t = 20.0
        while not stop_condition(self.stop_criterion, accuracy, generation_num, self.stop_value):
            # best fitness of the previous population
            old_best_fitness = population.best_fitness()
            # clean parents, children, mutation lists for the new population
            population.clean()
            # select even number of parents for recombination
            population.selection(self.selection_method, t)
            # lower the temperature for the next cycle
            if self.selection_method == 'annealing':
                t *= 0.5
            # create children
            population.recombination(self.recombination_method)
            # implement random mutations
            population.mutation(self.mutation_method, generation_num)
            # reducing the number of individuals to n_pop
            population.reduction(self.reduction_method)
            # calculate the best fitness of current population
            new_best_fitness = population.best_fitness()
            # compare results for possible cycle condition
            accuracy = abs(new_best_fitness - old_best_fitness)
            generation_num += 1
        print("The optimum value is:", population.final_chromosome().fitness_value)
        print("It is reached at the point:", population.final_chromosome().gene_list)
        return population.final_chromosome().fitness_value

