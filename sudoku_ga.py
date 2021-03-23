# Colin Francis
# Date: 3/10/2021
# Description: A class used to solve sudoku puzzles using a genetic algorithm
import random
import copy
import sudoku_board
# TODO: Add a data member to keep track of current iteration and the average fitness score.
# TODO: Consider having some kind of initialize method to create generation 1 and then from there begin the actual algo


class SudokuGeneticAlgorithm(object):
    def __init__(self, board):
        self._board_template = board
        self._population = []
        self._population_size = 1500
        self._generation = 0
        self._average_fitness = None
        self._crossover_rate = 80
        self._mutation_rate = 20
        self._fixed_values = []
        self._best_solution = None

    def print_boards(self):  # TODO: Remove
        for member in self.get_population():
            for row in member.get_board():
                print(row)
            print(member.get_fitness(), member.get_probability())
            print()

    def get_population(self):
        """Returns current members in the population."""
        return self._population

    def _create_initial_population(self, number: int) -> None:
        """Creates initial population to begin genetic algorithm."""
        for population_size in range(number):
            self._population.append(copy.deepcopy(sudoku_board.SudokuBoard(self._board_template)))

        for member in self._population:
            for row_index, row in enumerate(member.get_board()):
                for value_index, value in enumerate(row):
                    if value == '.':
                        member.get_board()[row_index][value_index] = str(random.randint(1, 9))

    @staticmethod
    def _board_transform(structure: str, member: list) -> list:
        """Transforms board columns and regions into row matrices."""
        member_transform = copy.deepcopy(member)
        if structure == "row":  # TODO: Probably don't need this since nothing new is being returned
            return member
        elif structure == "col":
            for row_index, row in enumerate(member):
                for value_index, value in enumerate(row):
                    member_transform[value_index][row_index] = value
            return member_transform
        else:
            for row_index, row in enumerate(member):
                for value_index, value in enumerate(row):
                    if row_index == 0 or row_index == 3 or row_index == 6:
                        if 2 < value_index <= 5:
                            member_transform[row_index + 1][value_index - 3] = value
                        else:
                            member_transform[row_index + 2][value_index - 6] = value
                    elif row_index == 1 or row_index == 4 or row_index == 7:
                        if value_index <= 2:
                            member_transform[row_index - 1][value_index + 3] = value
                        elif value_index >= 6:
                            member_transform[row_index + 1][value_index - 3] = value
                    elif row_index == 2 or row_index == 5 or row_index == 8:
                        if value_index <= 2:
                            member_transform[row_index - 2][value_index + 6] = value
                        elif 2 < value_index <= 5:
                            member_transform[row_index - 1][value_index + 3] = value
            return member_transform

    def _find_fitness(self, structure: str, member: list) -> int:
        """Determines the fitness score for each member in the population."""
        # target fitness is 243
        if structure == "row":  # TODO: Probably don't need this
            member = self._board_transform(structure, member)
        elif structure == "col":
            member = self._board_transform(structure, member)
        else:
            member = self._board_transform(structure, member)

        fitness = 0
        for row in member:
            for value_index, value in enumerate(row):
                for check_value_index, check_value in enumerate(row):
                    if value_index != check_value_index and value != check_value:
                        continue
                    elif value_index == check_value_index:
                        continue
                    else:
                        break
                else:
                    fitness += 1

        return fitness

    def _fitness_average(self):
        total_fitness = 0
        for member in self._population:
            total_fitness += member.get_fitness()
        self._average_fitness = total_fitness / self._population_size

    def _initial_population(self):
        """Randomly initializes the initial population."""
        for row_index, row in enumerate(self._board_template):
            for value_index, value in enumerate(row):
                if value != '.':
                    self._fixed_values.append([row_index, value_index])
        self._create_initial_population(self._population_size)
        for member in self._population:
            member.set_fitness(self._find_fitness("row", member.get_board()) +
                               self._find_fitness("col", member.get_board()) +
                               self._find_fitness("reg", member.get_board()))
        self._selection_probability()
        self._fitness_average()

    def _selection_probability(self):
        """Determines the probability that a member of the population is selected
        for mating based on their fitness score."""
        total_fitness = 0
        for member in self._population:
            total_fitness += member.get_fitness()

        for member in self._population:
            member.set_probability((member.get_fitness() / total_fitness) * 100)

    def _crossover(self):
        roulette_wheel = {}
        next_generation = []

        lower_bound = 0
        for member in self._population:
            roulette_wheel[member] = [lower_bound, lower_bound + member.get_probability()]
            lower_bound += member.get_probability()

        while len(next_generation) < self._population_size:
            parents = []
            for parent_selection in range(2):
                rand = random.uniform(0, 100)
                for member in roulette_wheel.keys():
                    if roulette_wheel[member][0] <= rand < roulette_wheel[member][1]:
                        parents.append(member)
                        break

            child_1 = copy.deepcopy(parents[0])
            child_2 = copy.deepcopy(parents[1])

            for row_index, row in enumerate(child_1.get_board()):
                if random.uniform(0, 100) >= 20:
                    child_1.get_board()[row_index] = parents[1].get_board()[row_index]
                    child_2.get_board()[row_index] = parents[0].get_board()[row_index]

            next_generation.append(child_1)
            next_generation.append(child_2)

        return next_generation

    def _sort_population(self):
        ranked_members = []
        for member in self._population:
            if not ranked_members:  # if ranked_population is empty
                ranked_members.append((member, member.get_fitness()))
            else:
                for index, ranked_member in enumerate(ranked_members):
                    if member.get_fitness() >= ranked_member[1]:
                        ranked_members.insert(index, (member, member.get_fitness()))
                        break
                    else:
                        continue
                else:
                    ranked_members.insert(len(ranked_members), (member, member.get_fitness()))
        return ranked_members

    def _selection(self):
        ranked_population = []
        ranked_members = self._sort_population()
        while len(ranked_members) > self._population_size:
            del ranked_members[len(ranked_members) - 1]

        for ranked_member in ranked_members:
            ranked_population.append(ranked_member[0])

        return ranked_population

    def solve(self):
        """Solves sudoku puzzle through implementation of genetic algorithm."""
        self._initial_population()  # develop initial population - generation 0
        print("Generation 0 Average Fitness", self._average_fitness)

        # Main Loop:
        for run in range(100):
            self._generation += 1
            children = self._crossover()
            for child in children:
                self._population.append(child)
            self._population = self._selection()

            for member in self._population:
                member.set_fitness(self._find_fitness("row", member.get_board()) +
                                   self._find_fitness("col", member.get_board()) +
                                   self._find_fitness("reg", member.get_board()))
                if self._best_solution is None:
                    self._best_solution = member
                else:
                    if member.get_fitness() > self._best_solution.get_fitness():
                        self._best_solution = member
            self._selection_probability()
            self._fitness_average()
            print("Generation {} Average Fitness: {}".format(self._generation, self._average_fitness))

        print(self._best_solution.get_fitness())
        for row in self._best_solution.get_board():
            print(row)
