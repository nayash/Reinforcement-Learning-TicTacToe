#
# Copyright 2019 Asutosh Nayak. All rights reserved.
#

"""
This script is the entry point for this application. This instantiates the Board
and start the game play/training. 
"""
from src.Board import Board
from src.QTPlayer import QTPlayer
from src.OtherPlayer import OtherPlayer
from src.MinMaxPlayer import MinMaxPlayer

q_player = QTPlayer()
o_player = MinMaxPlayer()  # OtherPlayer()

board = Board()
board.start_play(q_player, o_player, 1, 5)
print("------Game Finished------")
