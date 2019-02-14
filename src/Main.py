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
This script is the entry point for this application. This instantiates the Board
and start the game play/training. 
"""
from src.Board import Board
from src.QTPlayer import QTPlayer
from src.OtherPlayer import OtherPlayer
from src.MinMaxPlayer import MinMaxPlayer

q_player = QTPlayer()
o_player = MinMaxPlayer()  # OtherPlayer()
q_player.load_table()
board = Board()
board.start_play(q_player, o_player, 10, 500)
print("------Game Finished------")

