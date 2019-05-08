#
# Copyright (c) 2019. Asutosh Nayak (nayak.asutosh@ymail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#

"""
A Tic-Tac-Toe player implementation using MinMax algorithm.
reference : https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/
"""

import numpy as np
import time
import pickle

from Board import Board, NUM_CELLS, WIN_O, WIN_X, DRAW, _EMPTY_, _X_, _O_, IN_PROG
from PlayerBase import PlayerBase

WIN_VALUE = 10
LOSE_VALUE = -10
DRAW_VALUE = 10


class MinMaxPlayer(PlayerBase):

    def __init__(self, side: int = _O_):
        self.move_history = []
        self.side = side
        self.calc_move_cache = {}  # board_hash, best_move
        super().__init__()

    def make_move(self, board: Board):  # implementation would take a param: current "Board" instance
        """
        Called on MinMax player to calculate best move for give board. Calls find_best_move function internally.
        Returns best move cell and corresponding game value which can be ignored if not needed.
        :param board: instance of Board object
        :return: best_move_cell_index_1D: int, best_game_value: int
        """
        return self.find_best_move(board)[0]

    def match_over(self, match_result: int):
        """
        can be used to do post match calculations or clean-up
        :param match_result:
        :return: no return value
        """
        pass

    def next_match(self):
        self.move_history = []

    def get_other_side(self):
        if self.side == _X_:
            return _O_
        else:
            return _X_

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
                board.board[pos_coord] = self.get_other_side()
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
        stime = time.time()
        if board.is_over() != IN_PROG:
            print("Match already over")
            return -1, -1

        empty_cells = board.get_empty_cells_1d()
        best_value = -np.inf
        best_move = -1  # cell index in 1D for best move
        for cell in empty_cells:
            pos_coord = board.pos_1d_to_2d(cell)
            board.board[pos_coord] = self.side  # move to try
            board_hash = board.board_to_hash()
            if board_hash in self.calc_move_cache:
                calc_value = self.calc_move_cache[board_hash]
            else:
                calc_value = self.min_max(board, 0, False)
                self.calc_move_cache[board_hash] = calc_value
            board.board[pos_coord] = _EMPTY_  # undo move that was tried above
            if calc_value > best_value:
                best_value = calc_value
                best_move = cell
        self.move_history.append((board.board_to_hash(), best_move))
        if (time.time() - stime) > 4:
            print("Runtime for find_best_move", (time.time() - stime) // 60, "minutes", (time.time() - stime) % 60,
                  "seconds")
        return best_move, best_value

    def save_data(self):
        pass

    def load_data(self):
        pass
