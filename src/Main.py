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
from Board import Board, _X_, _O_
from QTPlayer import QTPlayer
from RandomPlayer import RandomPlayer
from MinMaxPlayer import MinMaxPlayer
from PseudoRandomPlayer import PseudoRandomPlayer

q_player = QTPlayer(_X_)
o_player = PseudoRandomPlayer()  # QTPlayer(_O_)
# q_player.load_data()
# o_player.load_data()
board = Board()
board.start_play(q_player, o_player, 100, 100)
print("------Game Finished------")

