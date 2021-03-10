# Colin Francis
# Date: 3/10/2021
# Description: A class used to solve sudoku puzzles using a genetic algorithm
import random
import copy
import sudoku_board

# TODO: Continue working on find_fitness method
# TODO: Create a solve function and make other function private


class SudokuGeneticAlgorithm(object):
    def __init__(self, board):
        self._board_template = board
        self._population = []

    def print_boards(self):  # TODO: Remove
        for member in self.get_population():
            for row in member.get_board():
                print(row)
            print(member.get_fitness())
            print()

    def get_population(self):
        return self._population

    def _create_population(self, number: int) -> None:
        for population_size in range(number):
            self._population.append(copy.deepcopy(sudoku_board.SudokuBoard(self._board_template)))

        for member in self._population:
            for row_index, row in enumerate(member.get_board()):
                for value_index, value in enumerate(row):
                    if value == '.':
                        member.get_board()[row_index][value_index] = str(random.randint(1, 9))

    @staticmethod
    def _board_transform(structure: str, member):
        member_transform = copy.deepcopy(member)
        if structure == "row":
            return member
        elif structure == "col":
            for row_index, row in enumerate(member):
                for value_index, value in enumerate(row):
                    member_transform[value_index][row_index] = value
            return member_transform

    def _find_fitness(self, structure: str, member: list):
        # fitness function is searching for unique values in rows, columns, regions - I think?
        # if a value is unique, add 1 to fitness
        # target fitness is 243
        # need to add row fitness, column fitness, and region fitness
        if structure == "row":
            member = self._board_transform(structure, member)
        elif structure == "col":
            member = self._board_transform(structure, member)
        else:
            pass

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

    def solve(self):
        self._create_population(10)
        for member in self._population:
            print(self._find_fitness("row", member.get_board()))
            print(self._find_fitness("col", member.get_board()))
            member.set_fitness(self._find_fitness("row", member.get_board()) +
                               self._find_fitness("col", member.get_board()))
            # break
