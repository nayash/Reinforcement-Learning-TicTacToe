"""
This script is the entry point for this application. This instantiates the Board
and start the game play/training. 
"""

import Board
import QTPlayer
import OtherPlayer

class Main:
	def __init__(self):
		self.q_player = new QTPlayer()
		self.o_player = new OtherPlayer()
		self.board = new Board(self.q_player, self.o_player)
		self.board.start_play()
		print("------Game Finished------")
