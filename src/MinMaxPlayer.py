#
# Copyright 2019 Asutosh Nayak. All rights reserved.
#

"""
A Tic-Tac-Toe player implementation using MinMax algorithm.
"""

import pickle
import numpy as np

from src.Board import Board, NUM_CELLS, WIN_O, WIN_X, DRAW, _EMPTY_, _X_, _O_
from src.PlayerBase import PlayerBase

WIN_VALUE = 10
LOSE_VALUE = -10
DRAW_VALUE = 10


class MinMaxPlayer(PlayerBase):

    def __init__(self, side: int=0):
        self.move_history = []
        self.side = side
        super().__init__()

    def make_move(self, board: Board):  # implementation would take a param: current "Board" instance
        """
        Called on MinMax player to calculate best move for give board. Calls find_best_move function internally.
        Returns best move cell and corresponding game value which can be ignored if not needed.
        :param board: instance of Board object
        :return: best_move_cell_index_1D: int, best_game_value: int
        """
        return self.find_best_move(board)

    def match_over(self, match_result: int):
        """
        can be used to do post match calculations or clean-up
        :param match_result:
        :return: no return value
        """
        pass

    def next_match(self):
        self.move_history = []

    def min_max(self, board: Board, depth: int, is_max: bool):
        """
        Implementation of MinMax algorithm to find best move in Tic-Tac-Toe for given board state by recursively calling
        for min/max player alternately.
        :param board: Board object -- representing the current board state
        :param depth: depth of current MinMax call
        :param is_max: current call is for Max player or Min player (chooses strategy).
        :return: int: best move for given board
        """

        result = board.is_over()
        if result == WIN_X:
            if self.side == _X_:
                return WIN_VALUE
            else:
                return LOSE_VALUE
        elif result == WIN_O:
            if self.side == _O_:
                return WIN_VALUE
            else:
                return LOSE_VALUE
        elif result == DRAW:
            return 0

        if is_max:
            best_value = -np.inf
            empty_cells = board.get_empty_cells_1d()
            for cell in empty_cells:
                pos_coord = board.pos_1d_to_2d(cell)
                board.board[pos_coord] = self.side
                best_value = np.maximum(best_value, self.min_max(board, depth+1, not is_max))
                board.board[pos_coord] = _EMPTY_
            return best_value-depth
        else:
            best_value = np.inf
            empty_cells = board.get_empty_cells_1d()
            for cell in empty_cells:
                pos_coord = board.pos_1d_to_2d(cell)
                board.board[pos_coord] = self.side
                best_value = np.minimum(best_value, self.min_max(board, depth+1, not is_max))
                board.board[pos_coord] = _EMPTY_
            return best_value-depth

    def find_best_move(self, board: Board):
        """
        This function mimics 'this' players move on each of the empty cells, and gets the final game value for each of
        them by calling 'min_max' function on each cell. It then chooses the best of all these values and hence best
        move.
        :return: int, int --> best move, game result
        """
        empty_cells = board.get_empty_cells_1d()
        best_value = -np.inf
        best_move = -1  # cell index in 1D for best move
        for cell in empty_cells:
            pos_coord = board.pos_1d_to_2d(cell)
            board.board[pos_coord] = self.side
            calc_value = self.min_max(board, 0, False)
            board.board[pos_coord] = _EMPTY_
            if calc_value > best_value:
                best_value = calc_value
                best_move = cell
        self.move_history.append((board.board_to_hash(), best_move))
        return best_move, best_value
