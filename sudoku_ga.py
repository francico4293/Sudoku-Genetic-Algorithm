# Colin Francis
# Date: 3/9/2021
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

    def create_population(self, number):
        for population_size in range(number):
            self._population.append(copy.deepcopy(sudoku_board.SudokuBoard(self._board_template)))

        for member in self._population:
            for row_index, row in enumerate(member.get_board()):
                for value_index, value in enumerate(row):
                    if value == '.':
                        member.get_board()[row_index][value_index] = str(random.randint(1, 9))

    def find_fitness(self):
        # fitness function is searching for unique values in rows, columns, regions - I think?
        # if a value is unique, add 1 to fitness
        # target fitness is 243
        # need to add row fitness, column fitness, and region fitness
        for member in self._population:
            row_fitness = 0
            for row in member.get_board():
                for value_index, value in enumerate(row):
                    for check_value_index, check_value in enumerate(row):
                        if value_index != check_value_index and value != check_value:
                            continue
                        elif value_index == check_value_index:
                            continue
                        else:
                            break
                    else:
                        row_fitness += 1
            member.set_fitness(row_fitness)