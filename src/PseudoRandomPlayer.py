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
This class uses MiniMax and Random strategy randomly to generate moves. Training against this player may
help fixing playing same board state repeatedly.
"""
import numpy as np

from src.Board import Board
from src.PlayerBase import PlayerBase
from src.MinMaxPlayer import MinMaxPlayer


class PseudoRandomPlayer(PlayerBase):

    def __init__(self):
        self.move_history = []
        self.min_max_player = MinMaxPlayer()
        super().__init__()

    def make_move(self, board: Board) -> int:
        randomizer = np.random.uniform(0.1, 0.9, 1)
        if randomizer >= 0.4:
            # use MiniMax strategy most of the time but randomize sometimes just like humans make mistake sometimes
            return self.min_max_player.find_best_move(board)[0]
        else:
            empty_cells = board.get_empty_cells_1d()
            while True:
                move = np.random.choice(empty_cells)
                if board.is_move_valid(move):
                    self.move_history.append(move)
                    return move

    def match_over(self, match_result):
        pass

    def next_match(self):
        self.move_history = []

    def save_data(self):
        pass

    def load_data(self):
        pass
