import random
import math

def stop_condition(stop_criterion, accuracy, generation_num, stop_value):
    """
    Based on stop_criterion, creates and checks the condition for the main cycle.

    :type stop_criterion: string
    :type accuracy: float
    :type generation_num: int
    :type stop_value: float
    :return: bool
    """
    if stop_criterion == 'generations_limit':
        return generation_num >= stop_value
    elif stop_criterion == 'fitness_stability':
        return accuracy < stop_value



def distance(p1, p2):
    """
    Returns distance between 2 points.

    :param p1: point [X1;Y1]
    :type p1: list of floats
    :param p2: point [X2;Y2]
    :type p2: list of floats
    :return: distance in float
    """
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[2]
    return math.sqrt(x_diff**2 + y_diff**2)


def total_distance(points):
    """
    Returns the route length, where route is determined by the order of points in a given list.
    The first point is also the last one.

    :param points: coordinates [X;Y] of cities to visit
    :type points: list of lists [float; float]
    :return: distance in float
    """
    n = len(points)
    res = 0
    for i in range(n - 1):
        d = distance(points[i], points[i+1])
        res += d
    res += distance(points[n-1], points[0])
    return res


def mix_points(points):
    """
    Changes the order of points (except the first point).

    :param points: coordinates [X;Y] of cities to visit
    :type points: list of lists [float; float]
    :return: list of lists [float; float]
    """
    res_list = [points[0]]
    elements_to_shuffle = points[1:]
    random.shuffle(elements_to_shuffle)
    for i in range(len(points) - 1):
        res_list.append(elements_to_shuffle[i])
    return res_list


def ranging(i, N):
    """
    Formula for the ranging selection to get the probability for each individual.

    :param i: index (starting from 1) of the individual in sorted df (by fitness)
    :type i: int
    :param N: number of individuals in population
    :type N: int
    :return: float
    """
    a = random.uniform(1, 2)
    b = 2 - a
    return (1 / N) * (a - (a - b) * ((i - 1) / (N - 1)))


def euler(fitness_value, T):
    """
    Part of the simulated annealing selection formula.

    :param fitness_value: individual's fitness value
    :type fitness_value: float
    :param T: temperature
    :type T: float
    :return: float
    """
    return pow(math.e, (fitness_value / T))


def simulated_annealing(euler_avg, euler_current, N):
    """
    Formula for the simulated annealing selection to get the probability for each individual.

    :param euler_avg: average value of euler function for the population
    :type euler_avg: float
    :param euler_current: individual's current value of euler function
    :type euler_current: float
    :param N: number of individuals in population
    :type N: int
    :return: float
    """
    return (1 / N) * (euler_current / euler_avg)
