# ======================================================================================================================
# author:   Xincong YANG
# date:     23 Dec. 2017
# email:    xincong.yang@outlook.com
# name:     NSGA_ii
# ======================================================================================================================
import numpy as np
import matplotlib.pyplot as plt
import time

COLORS = ['#1a1a1a', '#404040', '#808080', '#bfbfbf']


class Individual(object):
    # individual unit
    def __init__(self):
        self.genotype = None
        self.phenotype = None

        # non-dominated sorting
        self.rank = None
        self.domination_count = None
        self.dominated_solutions = set()

        # crowding distance sorting
        self.crowding_distance = None

    def set_genotype(self, new_genotype):
        self.genotype = new_genotype

    def set_phenotype(self, new_phenotype):
        self.phenotype = new_phenotype

class Population(object):
    # population unit
    def __init__(self):
        # a list to store individuals
        self.population = []
        # a multilevel list to store individuals
        self.fronts = []

    def __len__(self):
        return len(self.population)

    def __iter__(self):
        return self.population.__iter__()

    def append(self, new_individual):
        self.population.append(new_individual)

    def extend(self, new_individuals):
        self.population.extend(new_individuals)

    def contains(self, new_individual):
        if_contain = False
        for individual in self.population:
            if np.array_equal(new_individual.genotype, individual.genotype):
                if_contain = True
                break
        return if_contain

    def get_phenotypes(self):
        phenotypes = []
        for individual in self.population:
            phenotypes.append(individual.phenotype)
        return np.array(phenotypes)

    @property
    def max_phenotype(self):
        maximum = np.max(self.get_phenotypes(), axis=0)
        return maximum

    @property
    def min_phenotype(self):
        minimum = np.min(self.get_phenotypes(), axis=0)
        return minimum

class Problem(object):
    def __init__(self, W, b, c):
        """
        obj_1:          min sum(Wx - b) < 0
        obj_2:          min cx
        :param W:
        :param b:
        :param c:
        """
        self.W = W
        self.b = b
        self.c = c
        self.genotype_num = len(c)
        self.phenotype_num = 2
        assert W.shape == (b.shape[0], c.shape[0]), "Please input compatible W, b and c"

    def create_individual(self):
        individual = Individual()
        # generate a binary genotype
        genotype = np.random.randint(100, size=self.genotype_num) // 99
        individual.set_genotype(new_genotype=genotype)
        phenotype = self.function(individual)
        individual.set_phenotype(new_phenotype=phenotype)
        return individual

    def function(self, inidividual):
        x = inidividual.genotype
        non_cover = np.mean(np.dot(self.W, x) - self.b < 0)
        cost = np.dot(self.c, x)
        return np.array([non_cover, cost])

    def create_population(self, population_size):
        population = Population()
        while len(population) < population_size:
            individual = self.create_individual()
            # if new individual is different from individuals in population, then add
            if not population.contains(new_individual=individual):
                population.append(individual)
        return population

    def epsilon_dominates(self, individual_1, individual_2, epsilon=(0, 0)):
        phenotype_1 = individual_1.phenotype
        phenotype_2 = individual_2.phenotype
        epsilons = np.array(epsilon)
        # whether individual 1 dominates individual 2
        dominate_num = np.sum(phenotype_1 - (phenotype_2 + epsilons) < 0)
        if dominate_num > 0:
            return True
        else:
            return False

class NSGA_ii(object):
    # main algorithm
    def __init__(self, problem, population_size, select_size, mutate_size):
        self.problem = problem
        self.population_size = population_size
        self.select_size = select_size
        self.mutate_size = mutate_size

        print("==========>>> Initialize algorithm ... <<<==========")
        # initialize the first parent population and offspring population - 2n
        self.population = self.problem.create_population(population_size=self.population_size)
        # epsilon non-dominated_sorting
        self.epsilon_non_dominated_sorting(self.population)
        # corwding distance sorting
        for front in self.population.fronts:
            self.crowding_distance_sorting(front)
        # generate offspring
        self.offspring = self.generate_offspring(self.population)

    def evolve(self, num_of_generations, ax):
        durations = []
        for i in range(num_of_generations):
            start = time.time()
            # main loop
            # combine
            self.population.extend(self.offspring)
            # epsilon non-dominated_sorting
            self.epsilon_non_dominated_sorting(self.population)

            new_population = Population()
            front_num = 0

            # corwding distance sorting
            while len(new_population) + len(self.population.fronts[front_num]) < self.population_size:
                self.crowding_distance_sorting(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1

            # fill up
            self.crowding_distance_sorting(self.population.fronts[front_num])
            new_population.extend(self.population.fronts[front_num][:self.population_size - len(new_population)])

            self.population = new_population

            # generate new offspring
            self.offspring = self.generate_offspring(self.population)

            duration = time.time() - start
            durations.append(duration)
            print("==========>>> Evolution: [%d / %d] Time: %.3f sec <<<==========" % (i, num_of_generations, duration))

            if ax:
                if i % 10 == 0:
                    self.plot(ax=ax, color=str(1 - i/num_of_generations))

        durations = np.array(durations)

        return self.population, durations

    def epsilon_non_dominated_sorting(self, population):
        population.fronts = []
        population.fronts.append([])

        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = set()

            for other_individual in population:
                if self.problem.epsilon_dominates(individual_1=individual, individual_2=other_individual):
                    individual.dominated_solutions.add(other_individual)
                elif self.problem.epsilon_dominates(individual_1=other_individual, individual_2=individual):
                    individual.domination_count += 1

            if individual.domination_count == 0:
                population.fronts[0].append(individual)
                individual.rank = 0

        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i + 1
                        temp.append(other_individual)
            i = i + 1
            population.fronts.append(temp)

    def crowding_distance_sorting(self, front):
        if len(front) == 1:
            front[0].crowding_distance = self.problem.phenotype_num
        elif len(front) >= 2:
            for individual in front:
                individual.crowding_distance = 0
            for i in range(self.problem.phenotype_num):
                if i == 0:
                    # ascending sorted from small to big
                    front = sorted(front, key=lambda p: p.phenotype[i])
                    front[0].crowding_distance += self.problem.phenotype_num
                    front[-1].crowding_distance += self.problem.phenotype_num
                    for j in range(1, len(front) - 1):
                        front[i].crowding_distance += (front[j - 1].crowding_distance - front[j + 1].crowding_distance) / \
                                                      (self.population.max_phenotype[i] - self.population.min_phenotype[i])
        # sort front according to crowding distance
        front = sorted(front, key=lambda p: - p.crowding_distance)

    def generate_offspring(self, population):
        offspring = []
        while len(offspring) < self.population_size:
            # select
            parent_1 = self._select(population)
            parent_2 = self._select(population)
            while np.array_equal(parent_1.genotype, parent_2.genotype):
                parent_2 = self._select(population)

            # crossover
            child_1, child_2 = self._crossover(parent_1, parent_2)

            # mutate
            self._mutate(child_1)
            self._mutate(child_2)

            if not population.contains(child_1):
                phenotype_1 = self.problem.function(child_1)
                child_1.set_phenotype(phenotype_1)
                offspring.append(child_1)

            if len(offspring) == self.population_size:
                break

            if not population.contains(child_2):
                phenotype_2 = self.problem.function(child_2)
                child_2.set_phenotype(phenotype_2)
                offspring.append(child_2)
        return offspring

    def _crowding_operator(self, individual_1, individual_2):
        if individual_1.rank < individual_2.rank or (individual_1.rank == individual_2.rank
                                                     and individual_1.crowding_distance > individual_2.crowding_distance):
            return True
        else:
            return False

    def _select(self, population):
        participant_indices = np.random.choice(np.arange(self.population_size), size=self.select_size)
        participants = [population.population[i] for i in participant_indices]
        best_one = None
        for participant in participants:
            if best_one == None or self._crowding_operator(participant, best_one):
                best_one = participant
        return best_one

    def _crossover(self, individual_1, individual_2):
        child_1 = self.problem.create_individual()
        child_2 = self.problem.create_individual()
        num = self.problem.genotype_num
        crossover_indices = np.random.choice(np.arange(num), size=num // 2)
        for i in range(num):
            if i in crossover_indices:
                child_1.genotype[i] = individual_2.genotype[i]
                child_2.genotype[i] = individual_1.genotype[i]
            else:
                child_1.genotype[i] = individual_1.genotype[i]
                child_2.genotype[i] = individual_2.genotype[i]
        return child_1, child_2

    def _mutate(self, individual):
        num = self.problem.genotype_num
        mutate_indices = np.random.choice(np.arange(num), size=self.mutate_size)
        for i in mutate_indices:
            individual.genotype[i] = 1 - individual.genotype[i]

    def plot(self, ax, color=None):
        self.epsilon_non_dominated_sorting(self.population)
        for i, front in enumerate(self.population.fronts):
            for individual in front:
                if color == None:
                    ax.scatter(1 - individual.phenotype[0], individual.phenotype[1], s=5, color=COLORS[i // 4])
                else:
                    ax.scatter(1 - individual.phenotype[0], individual.phenotype[1], s=5, color=color)

if __name__ == '__main__':
    W = np.load('A.npy').T
    b = np.load('b.npy')
    c = np.load('c.npy')

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    problem = Problem(W=W, b=b, c=c)
    nsga = NSGA_ii(problem=problem, population_size=200, select_size=20, mutate_size=20)
    population, times = nsga.evolve(num_of_generations=1000, ax=ax)

    plt.show()


