# Colin Francis
# Date: 3/10/2021
# Description: A class representing a sudoku board
class SudokuBoard(object):
    def __init__(self, board):
        self._board = board
        self._fitness = None
        self._probability = None

    def get_board(self):
        return self._board

    def get_fitness(self):
        return self._fitness

    def get_probability(self):
        return self._probability

    def set_fitness(self, fitness):
        self._fitness = fitness

    def set_probability(self, probability):
        self._probability = probability
