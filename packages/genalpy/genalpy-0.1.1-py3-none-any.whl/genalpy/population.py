import numpy as np
import pandas as pd
from genalpy.utils import mix_points, ranging, euler, simulated_annealing
from genalpy.chromosome import Chromosome
import random


class Population:
    """
    Instantiates the population - set of individuals. Each individual has one chromosome.

    :param chromosome_list: current individuals
    :type chromosome_list: list of objects (Chromosomes)
    :param parents_list: selected parents
    :type parents_list: list of objects (Chromosomes)
    :param children_list: non-mutated children
    :type children_list: list of objects (Chromosomes)
    :param mutation_list: mutated children
    :type mutation_list: list of objects (Chromosomes)
    """
    def __init__(self, task_type, n_pop, fitness_func, goal, dimensions,
                 boundaries, points):
        self.task_type = task_type
        self.n_pop = n_pop
        self.fitness_func = fitness_func
        self.goal = goal
        self.dimensions = dimensions
        self.boundaries = boundaries
        self.points = points
        self.chromosome_list = []
        self.parents_list = []
        self.children_list = []
        self.mutation_list = []

    def clean(self):
        """
        Prepare population to the next step (empty parents, children, mutation lists).
        """
        self.parents_list = []
        self.children_list = []
        self.mutation_list = []

    def create(self, create_population_method, focus_boundaries):
        """
        Generates random chromosomes and fills the first population with them.
        """
        if create_population_method == 'shotgun':
            bound = self.boundaries
        elif create_population_method == 'focusing':
            bound = focus_boundaries
        else:
            print('Try available methods')
        for i in range(self.n_pop):
            if self.task_type == 'func_extremum':
                if self.dimensions == 2:
                    new_chromosome = Chromosome([np.random.uniform(bound[0], bound[1])],
                                                self.fitness_func)
                elif self.dimensions == 3:
                    new_chromosome = Chromosome([np.random.uniform(bound[0], bound[1]),
                                                 np.random.uniform(bound[2], bound[3])],
                                                self.fitness_func)
            elif self.task_type == 'TSP':
                new_chromosome = Chromosome(mix_points(self.points), self.fitness_func)
            self.chromosome_list.append(new_chromosome)

    def selection(self, selection_method, t):
        """
        Selects mostly the best individuals for recombination and puts them in parents_list.
        Number of parents is the half of n_pop.
        Proportional method is used only for maximization and positive fitness values.
        Ranging and simulated annealing for both max & min, and any fitness values.

        :param t: temperature for the simulated annealing
        :param t: float
        """
        # create DataFrame with chromosomes and their fitness_values to operate
        df_proportions = pd.DataFrame({'chromosome': self.chromosome_list,
                                       'fitness': [ch.fitness_value for ch in self.chromosome_list]})
        if selection_method == 'proportional':
            sum_fitness = sum(df_proportions['fitness'])
            # get the proportional fitness -> probability
            df_proportions['probability'] = df_proportions.apply((lambda row: (row['fitness'] / sum_fitness)), axis=1)
        elif selection_method == 'ranging':
            df_proportions.sort_values(by='fitness', ascending=False, inplace=True)
            # get the i - index
            df_proportions.reset_index(drop=False, inplace=True)
            df_proportions['probability'] = df_proportions.apply(lambda row: (ranging(row['index'] + 1, self.n_pop)),
                                                                 axis=1)
            # get rid of extra column
            df_proportions.drop(columns='index', inplace=True)
        elif selection_method == 'annealing':
            df_proportions['euler'] = df_proportions.apply(lambda row: (euler(row['fitness'], t)),
                                                                 axis=1)
            euler_avg = float(df_proportions['euler'].mean())
            df_proportions['probability'] = df_proportions.apply(lambda row: (simulated_annealing(euler_avg, row['euler'],
                                                                                                  self.n_pop)),
                                                                 axis=1)
        # sort and cumsum the probabilities to 'place' them on the line segment
        df_proportions.sort_values(by='probability', ascending=False, inplace=True)
        df_proportions['probability_cumulative'] = df_proportions['probability'].cumsum()
        df_proportions.reset_index(drop=True, inplace=True)
        # get the start of each segment (it will be the end of the previous segment)
        probs_offset = list(df_proportions['probability_cumulative'])
        probs_offset = [0.0] + probs_offset[:-1]
        df_proportions['probability_lower_limit'] = probs_offset
        # generate numbers on the line [0;1] and sort them asc
        random_list = [np.random.uniform(0, 1) for i in range(int(self.n_pop / 2))]
        random_list.sort()
        # get the parent based on generated number
        for num in random_list:
            # num must be between chromosomes boundaries
            df_proportions['parent'] = np.where((df_proportions['probability_lower_limit'] <= num) &
                                                (df_proportions['probability_cumulative'] > num), True, False)
            # add parent chromosome to the list
            try:
                parent_ch = df_proportions[df_proportions.parent].reset_index(drop=True)['chromosome'].iloc[0]
                self.parents_list.append(parent_ch)
            except:
                pass
        # drop duplicates
        self.parents_list = list(set(self.parents_list))
        # parents must form pairs -> get even number of them
        if len(self.parents_list) % 2 != 0:
            self.parents_list = self.parents_list[:-1]

    def recombination(self, recombination_method):
        """
        Generates new individuals based on chosen parents and puts them in children_list.
        Discrete - get the genes from each parent based on mask.
        """
        num_of_parents = len(self.parents_list)
        pairs_list = []
        selected_parents_list = []
        while len(selected_parents_list) < num_of_parents:
            # get parents from non-selected
            first_parent = random.choice([parent for parent in self.parents_list if parent not in selected_parents_list])
            selected_parents_list.append(first_parent)
            second_parent = random.choice([parent for parent in self.parents_list if parent not in selected_parents_list])
            selected_parents_list.append(second_parent)
            # create and add pair to list
            pair = [first_parent, second_parent]
            pairs_list.append(pair)
        chromosome_len = len(self.chromosome_list[0].gene_list)
        if recombination_method == 'discrete':
            for parent_pair in pairs_list:
                chromosome_genes = []
                for i in range(chromosome_len):
                    # choose the gene, 0 - first parent, 1 - second parent
                    mask = random.randint(0, 1)
                    if mask == 0:
                        chromosome_genes.append(parent_pair[0].gene_list[i])
                    else:
                        chromosome_genes.append(parent_pair[1].gene_list[i])
                self.children_list.append(Chromosome(chromosome_genes, self.fitness_func))
        elif (recombination_method == 'transitional') or (recombination_method == 'linear'):
            for parent_pair in pairs_list:
                chromosome_genes_first = []
                chromosome_genes_second = []
                if recombination_method == 'linear':
                    beta1 = random.uniform(0, 1.25)
                    beta2 = random.uniform(0, 1.25)
                for i in range(chromosome_len):
                    if recombination_method == 'transitional':
                        beta1 = random.uniform(0, 1.25)
                        beta2 = random.uniform(0, 1.25)
                    p1 = parent_pair[0].gene_list[i]
                    p2 = parent_pair[1].gene_list[i]
                    chromosome_genes_first.append(p1 + beta1 * (p2 - p1))
                    chromosome_genes_second.append(p1 + beta2 * (p2 - p1))
                self.children_list.append(Chromosome(chromosome_genes_first, self.fitness_func))
                self.children_list.append(Chromosome(chromosome_genes_second, self.fitness_func))

    def mutation(self, mutation_method, generation_num):
        """
        Randomly picks up some individuals from children_list and implements the certain type of gene mutation.
        """
        mutation_probability = 0.1 - (1 / (self.n_pop * 10)) * generation_num
        if mutation_method == 'real_number':
            for child in self.children_list:
                mutate = (random.random() <= mutation_probability)
                if mutate:
                    self.children_list.remove(child)
                    chromosome_len = len(child.gene_list)
                    chromosome_genes = []
                    for i in range(chromosome_len):
                        modified_gene = random.uniform(self.boundaries[i*2], self.boundaries[i*2 + 1])
                        chromosome_genes.append(modified_gene)
                    self.mutation_list.append(Chromosome(chromosome_genes, self.fitness_func))

    def reduction(self, reduction_method):
        """
        Chooses some individuals and deletes them from the current population.
        """
        # select the rest part of individuals (not parents)
        population_remainder = [ch for ch in self.chromosome_list if ch not in self.parents_list]
        all_population = population_remainder + self.parents_list + self.children_list + self.mutation_list
        if reduction_method == 'selective_scheme':
            df_population = pd.DataFrame({'chromosome': all_population,
                                          'fitness_value': [ch.fitness_value for ch in all_population]})
            if self.goal == 'min':
                df_population.sort_values(by='fitness_value', ascending=True, inplace=True)
            elif self.goal == 'max':
                df_population.sort_values(by='fitness_value', ascending=False, inplace=True)
            df_population.reset_index(drop=True, inplace=True)
            df_population = df_population[:self.n_pop]
            clean_population = list(df_population['chromosome'])
        elif reduction_method == 'uniform_random_replacement':
            num_to_delete = len(all_population) - self.n_pop
            items_to_delete = set(random.sample(range(len(all_population)), num_to_delete))
            clean_population = [x for i, x in enumerate(all_population) if not i in items_to_delete]
        self.chromosome_list = clean_population

    def best_fitness(self):
        """
        Get the best fitness value among all current chromosomes.

        :return: float
        """
        # in case of the first generation - empty list
        if not self.chromosome_list:
            return 0.0
        fitness_values_list = [ch.fitness_value for ch in self.chromosome_list]
        if self.goal == 'min':
            return min(fitness_values_list)
        elif self.goal == 'max':
            return max(fitness_values_list)


    def final_chromosome(self):
        """
        Get the result chromosome with the optimum fitness.

        :return: Chromosome
        """
        if not self.chromosome_list:
            return None
        df_final_population = pd.DataFrame({'chromosome': self.chromosome_list,
                                      'fitness_value': [ch.fitness_value for ch in self.chromosome_list]})
        if self.goal == 'min':
            df_final_population.sort_values(by='fitness_value', inplace=True, ascending=True)
        elif self.goal == 'max':
            df_final_population.sort_values(by='fitness_value', inplace=True, ascending=False)
        df_final_population.reset_index(drop=True, inplace=True)
        return df_final_population['chromosome'].iloc[0]



