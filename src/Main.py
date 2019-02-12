#
# Copyright 2019 Asutosh Nayak. All rights reserved.
#

"""
This script is the entry point for this application. This instantiates the Board
and start the game play/training. 
"""
from src.Board import Board
# from src.QTPlayer import QTPlayer
# from src.OtherPlayer import OtherPlayer

# q_player = QTPlayer.QTPlayer()
# o_player = OtherPlayer.OtherPlayer()

board = Board()
board.start_play(1, 5)
print("------Game Finished------")
