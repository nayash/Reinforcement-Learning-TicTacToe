#
# Copyright 2019 Asutosh Nayak. All rights reserved.
#

"""
This is the other player which plays with QTPlayer.
"""
import numpy as np

from src.Board import Board
from src.PlayerBase import PlayerBase


class OtherPlayer(PlayerBase):

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
