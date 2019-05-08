"""
This is just scratch pad.
"""

import pickle
import numpy as np

from Board import Board, NUM_CELLS, WIN_O, WIN_X, DRAW, _X_, _O_
from QTPlayer import QTPlayer
from MinMaxPlayer import MinMaxPlayer

board = Board()
q_player = QTPlayer()

q_player.load_table()
mm_player = MinMaxPlayer(_O_)
board.board = np.asarray([[1, 0, 1],
                          [0, 0, -1],
                          [1, 1, -1]])
print("Calculated move", q_player.make_move(board))
# board.load_anim_data()
# board.start_visual()
print(q_player.get_q_value(board.board_to_hash()))

import tempfile
print(tempfile.gettempdir())

import matplotlib
print(matplotlib.__version__)