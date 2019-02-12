#
# Copyright 2019 Asutosh Nayak. All rights reserved.
#

"""
This is the crux of this application. This class holds the code for Q-Learning.
Base class: PlayerBase
"""

import pickle
import numpy as np

from src.Board import Board, NUM_CELLS, WIN_O, WIN_X, DRAW
from src.PlayerBase import PlayerBase

OUTPUT_PATH = ".\\output\\"
OUTPUT_FILE_NAME = "q_table.pickle"

WIN_VALUE = 1.0
DRAW_VALUE = 0.5
LOSE_VALUE = 0.0

MIN_Q_VALUE = -9999


class QTPlayer(PlayerBase):

    def __init__(self, alpha=0.9, gamma=0.95, q_init=0.6):
        self.q_table = {}  # type: Dict[string, [float]]. Stores QValues for all actions for each state of board.
        self.moves_history = []  # type: [(board_hash: int, move: int)]
        self.alpha = alpha
        self.gamma = gamma
        self.q_init = q_init
        super().__init__()

    def save_table(self):
        """ saves the q_table into 'output' folder of application. """
        pickle.dump(self.q_table, open(OUTPUT_PATH+OUTPUT_FILE_NAME, "wb"))
        print("output saved. Length of table=", len(self.q_table))

    def load_table(self, table: dict = None):
        """implementation would take a parameter for QTable of type dict[int,[float]]"""
        if table is None:
            try:
                self.q_table = pickle.load(open(OUTPUT_PATH+OUTPUT_FILE_NAME, "rb"))
                print("Table loaded from output file. Length=", len(self.q_table))
            except FileNotFoundError:
                print("Either provide a QTable dict to load or a path from where QTable dict can be loaded")
        else:
            self.q_table = table
            print("Table loaded from passed object")

    def make_move(self, board: Board) -> int:
        """ function to make a move based on the """
        board_hash = board.board_to_hash()
        q_vals = self.get_q_value(board_hash)
        # print("init q_vals", q_vals)
        check_count = 0
        while check_count < NUM_CELLS:
            move = np.argmax(q_vals)  # gives action/cell which has max Q-Value
            # print("checking move", move)
            if board.is_move_valid(move):
                self.moves_history.append((board_hash, move))
                # print("Move made", (board_hash, move), "history len",len(self.moves_history))
                return move
            q_vals[move] = MIN_Q_VALUE
            check_count = check_count + 1

        # if no move found among q_vals, which shouldn't happen because 'make_move'
        # is called after checking if EMPTY cells are available
        print("Q-Values", q_vals, "\n", board_hash, "\n", str(board.board), check_count)
        raise Exception("No valid moves found")

    def get_q_value(self, board_hash: int):
        """
        Returns list of Q-Values for all possible actions for board state represented
        by hash value - board_hash
        """
        if board_hash not in self.q_table:
            # print("hash not found", board_hash)
            self.q_table[board_hash] = np.around(np.random.uniform(0.3, 0.7, 9), decimals=2)
            # np.full((NUM_CELLS,), self.q_init)
        return self.q_table[board_hash].copy()

    def update_q_table(self):
        pass

    def match_over(self, match_result: int):
        """
        Match is over. Update the Q-Learning Table as for all the moves in move history
        """
        print("Re-evaluating for result", match_result)
        self.moves_history.reverse()
        final_val = -1  # final state should be WIN_VALUE if q_player won, else other values
        if match_result == WIN_X:
            final_val = WIN_VALUE
        elif match_result == WIN_O:
            final_val = LOSE_VALUE
        else:
            final_val = DRAW_VALUE

        # old_value = self.q_table[self.moves_history[0][0]][self.moves_history[0][1]]
        self.q_table[self.moves_history[0][0]][self.moves_history[0][1]] = final_val
        # new_value = self.q_table[self.moves_history[0][0]][self.moves_history[0][1]]
        # print("Move made=", self.moves_history[0][1], ", Old Value=", old_value, ", New Value=", new_value,
        # "diff=", (new_value-old_value))
        for i, move in enumerate(self.moves_history[1:]):
            # Next board state of i^th move is (i-1)^th state, since we have reversed the moves history list.
            max_q_of_next_state = np.max(self.get_q_value(self.moves_history[i-1][0]))
            # key error!!! try saving all the keys in a list in get_hash function and check what's wrong.
            try:
                # old_value = self.q_table[move[0]][move[1]]
                self.q_table[move[0]][move[1]] = (1-self.alpha)*self.q_table[move[0]][move[1]] + self.alpha*self.gamma\
                    * max_q_of_next_state
                # new_value = self.q_table[move[0]][move[1]]
                # print("Move made=", move[1], ", Old Value=", old_value, ", New Value=", new_value, "diff=",
                # (new_value-old_value))
            except KeyError:
                print("Problem move is", move, self.q_table[move[0]] if move[0] in self.q_table else "key doesn't exist"
                      , "total hashes", len(self.q_table), "index", i)
                raise Exception("Key not found")

    def next_match(self):
        self.moves_history = []


