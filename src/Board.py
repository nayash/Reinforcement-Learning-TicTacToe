#
# Copyright 2019 Asutosh Nayak. All rights reserved.
#

import numpy as np

import QTPlayer as q_player
import OtherPlayer as o_player

class Board:
	"""
	This represents the board on which Tic-Tac-Toe is played.
	It includes the current state of the board instance and methods to 
	enforce game rules.
	"""

	# values to fill in board cell for each state are as follows:
	_X_ = 1
	_O_ = 0
	_EMPTY_ = -1

	# game states
	WIN_X = X
	WIN_O = O
	DRAW = 2
	IN_PROG = 3

	def __init__(self, turn=X, q_player, o_player):
		self.board = np.full((3,3), -1)
		self.turn = turn
		self.q_player = q_player # Q Learning player
		self.o_player = o_player # Other player (could be random or min-max)

	def is_over(self):
		"""
		checks if match is over.
		return: if 'X' wins X (=1), if 'O' wins O (=0), 
		"""
		temp_board = self.board.flatten()
        diag_m = np.take(temp_board,[0,4,8]) # np.diag(self.board)
        diag_s = np.take(temp_board,[2,4,6]) # np.diag(np.fliplr(self.board))
        mat = self.board # np.reshape(temp_board,(3,3))
        if ((mat == _X_).all(axis = 0).any() or (mat == _X_).all(axis = 1).any() or (diag_m == _X_).all()):
            return WIN_X # playerX win
        
        if((mat == _O_).all(axis = 0).any() or (mat == _O_).all(axis = 1).any() or (diag_m == _O_).all()):
            return WIN_O # playerO win
        
        if(np.count_nonzero(mat == _EMPTY_) == 0)
        	return DRAW # all cells filled but no one won; hence draw

        return -1 

    def start_play(self, tournaments=10, matches=100):
    	"""
		starts playing the game for passed number of tournaments, with each tournament
		having given number of matches. Uses the player passed while class instantiation.
    	"""
    	