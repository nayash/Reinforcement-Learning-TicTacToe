"""
This is the crux of this application. This class holds the code for Q-Learning.
Base class: PlayerBase
"""

import pickle
import numpy as np

import PlayerBase
import Board

OUTPUT_PATH = ".\\output\\"
OUTPUT_FILE_NAME = "q_table.pickle"

WIN_VALUE = 10.0
DRAW_VALUE = 5.0
LOSE_VALUE = 0.0

class QTPlayer(PlayerBase):

	MIN_Q_VALUE = -9999

	def __init__(self, alpha=0.9, gamma=0.95, q_init=0.6):
		self.q_table = {} # type: Dict[string, [float]]. Stores QValues for all possible actions for each state of the board.
		self.moves_history = [] # type: [(board_hash: int, move: int)] , 
		self.alpha = alpha
		self.gamma = gamma
		self.q_init = q_init
		
	def save_table(self):
		""" saves the q_table into 'output' folder of application. """
		 pickle.dump(self.q_table,open(OUTPUT_PATH+OUTPUT_FILE_NAME,"wb"))

	def load_table(self, table: dict = None): 
		"""implementation would take a parameter for QTable of type dict[int,[float]]"""
		if(table == None):
			try:
				self.q_table = pickle.load(open(OUTPUT_PATH+OUTPUT_FILE_NAME,"rb"))
			except FileNotFoundError:
				print("Either provide a QTable dict to load or a path from where QTable dict can be loaded")
		else:
			self.q_table = table

	def make_move(self, board_hash: int, board: Board):
		"""
		function to make a move based on the 
		"""
		q_vals = self.get_q_value(board_hash)
		check_count = 0
		while check_count < Board.NUM_CELLS:
			move = np.argmax(q_vals) # gives action/cell which has max Q-Value
			if(board.is_move_valid(move)):
				self.moves_history.append((board_hash,move))
				return move
			q_vals[move] = MIN_Q_VALUE
			check_count = check_count + 1

		# if no move found among q_vals, which shouldn't happen because 'make_move' is called after checking if EMPTY cells are available
		raise Exception("No valid moves found")
		print("Q-Values",q_vals,"\n",board_hash,"\n",str(board.board))



	def get_q_value(self, board_hash: int):
		""" 
		Returns list of Q-Values for all possible actions for board state represented
		by hash value - board_hash
		"""
		if(board_hash not in self.q_table):
			self.q_table[board_hash] = np.full((Board.NUM_CELLS,), self.q_init)
			
		return self.q_table[board_hash]

	def update_q_table(self):
		pass

	def match_over(self, match_result: int):
		"""
		Match is over. Update the Q-Learning Table as for all the moves in move history
		"""
		self.moves_history.reverse()
		final_val = -1 # final state should be WIN_VALUE if q_player won else other values
		if(match_result == Board.WIN_X):
			final_val = WIN_VALUE
		elif(match_result == Board.WIN_O):
			final_val = LOSE_VALUE
		else:
			final_val = DRAW_VALUE

		


