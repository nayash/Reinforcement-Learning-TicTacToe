import pickle
import numpy as np

from src.Board import Board, NUM_CELLS, WIN_O, WIN_X, DRAW
from src.QTPlayer import QTPlayer

board = Board()
q_player = QTPlayer()

q_player.load_table()
board.board = mat = np.asarray([[1, 0, 1],
                                [0, 1, 0],
                                [-1, -1, -1]])
print("Calculated move", q_player.make_move(board))

