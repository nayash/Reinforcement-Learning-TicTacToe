import pickle
import numpy as np

from src.Board import Board, NUM_CELLS, WIN_O, WIN_X, DRAW, _X_, _O_
from src.QTPlayer import QTPlayer
from src.MinMaxPlayer import MinMaxPlayer

board = Board()
q_player = QTPlayer()

q_player.load_table()
mm_player = MinMaxPlayer(_X_)
board.board = np.asarray([[1, -1, -1],
                          [-1, 0, -1],
                          [0, -1, 1]])
print("Calculated move", mm_player.make_move(board))

