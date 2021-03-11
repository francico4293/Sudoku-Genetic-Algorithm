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
        self._population_size = 5

    def print_boards(self):  # TODO: Remove
        for member in self.get_population():
            for row in member.get_board():
                print(row)
            print(member.get_fitness())
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
            for something in range(2):
                probability = random.uniform(0, 100)
                for member in roulette_wheel.keys():
                    if roulette_wheel[member][0] <= probability < roulette_wheel[member][1]:
                        parents.append(member)

            if parents[0].get_fitness() > parents[1].get_fitness():
                child = parents[0].get_board()[:6] + parents[1].get_board()[6:]
            else:
                child = parents[1].get_board()[:6] + parents[0].get_board()[6:]

            next_generation.append(child)

    def _mutation(self):
        pass

    def solve(self):
        """Solves sudoku puzzle through implementation of genetic algorithm."""
        self._create_initial_population(self._population_size)
        for member in self._population:
            member.set_fitness(self._find_fitness("row", member.get_board()) +
                               self._find_fitness("col", member.get_board()) +
                               self._find_fitness("reg", member.get_board()))
        self._selection_probability()
        self._crossover()
