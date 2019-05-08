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
This is a Random player which plays with QTPlayer.
"""
import numpy as np

from Board import Board
from PlayerBase import PlayerBase


class RandomPlayer(PlayerBase):

	def __init__(self):
		self.move_history = []
		super().__init__()

	def make_move(self, board: Board) -> int:
		empty_cells = board.get_empty_cells_1d()
		while True:
			move = np.random.choice(empty_cells)
			if(board.is_move_valid(move)):
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
