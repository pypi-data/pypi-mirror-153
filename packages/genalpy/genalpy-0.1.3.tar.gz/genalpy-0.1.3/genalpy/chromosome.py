class Chromosome:
    """
    Instantiates the chromosome - an individual's set of genes.

    :param gene_list: set of genes (mostly floats)
    :type gene_list: list

    :param fitness_func: lambda function to maximize/minimize
    :type fitness_func: function
    """
    def __init__(self, gene_list, fitness_func):
        self.gene_list = gene_list
        self.fitness_func = fitness_func
        # calculate fitness_value of the individual
        self.fitness_value = self.fitness_func(self.gene_list)

    def get_info(self):
        """
        Returns list of genes and the value of chromosome's fitness function
        """
        return self.gene_list, self.fitness_value
