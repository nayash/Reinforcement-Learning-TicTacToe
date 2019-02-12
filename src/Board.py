#
# Copyright 2019 Asutosh Nayak. All rights reserved.
#

import numpy as np

# values to fill in board cell for each state are as follows:
_X_ = 1
_O_ = 0
_EMPTY_ = -1

# game states
WIN_X = _X_
WIN_O = _O_
DRAW = 2
IN_PROG = 3

BOARD_DIM = (3, 3)
NUM_CELLS = BOARD_DIM[0] * BOARD_DIM[1]


class Board:
    """
    This represents the board on which Tic-Tac-Toe is played.
    It includes the current state of the board instance and methods to
    enforce game rules.
    """

    def __init__(self, turn=_X_):
        self.board = np.full((3, 3), _EMPTY_)
        self.turn = turn
        # self.q_player = q_player  # Q Learning player
        # self.o_player = o_player  # Other player (could be random or min-max)
        self.tournaments_stat = []

    def reset(self, turn=_X_):
        """
        reset all board variables for a new game
        """
        self.board = np.full((3, 3), _EMPTY_)
        self.turn = turn
        self.tournaments_stat = []

    def is_over(self):
        """
        checks if match is over.
        return: if 'X' wins X (=1), if 'O' wins O (=0),
        """
        temp_board = self.board.flatten()
        diag_m = np.take(temp_board, [0, 4, 8])  # np.diag(self.board)
        diag_s = np.take(temp_board, [2, 4, 6])  # np.diag(np.fliplr(self.board))
        mat = self.board  # np.reshape(temp_board,(3,3))
        if (mat == _X_).all(axis=0).any() or (mat == _X_).all(axis=1).any() or (diag_m == _X_).all() or (diag_s == _X_).all():
            return WIN_X  # playerX win

        if (mat == _O_).all(axis=0).any() or (mat == _O_).all(axis=1).any() or (diag_m == _O_).all() or (diag_s == _O_).all():
            return WIN_O  # playerO win

        if np.count_nonzero(mat == _EMPTY_) == 0:
            return DRAW  # all cells filled but no one won; hence draw

        return IN_PROG

    def start_play(self, q_player, o_player, tournaments=10, matches=100):
        """
        Starts playing the game for passed number of tournaments, with each tournament
        having given number of matches. Uses the player passed while class instantiation.
        For simpliciy let q-player always play 'X' irrespective of the fact that it's first player or not.
        """
        # deferred import due to cyclic dependency
        # from src.QTPlayer import QTPlayer
        # from src.OtherPlayer import OtherPlayer
        # self.q_player = QTPlayer()
        # self.o_player = OtherPlayer()

        print("Starting Game...")
        self.match_results = np.full((tournaments, matches), -1)
        for t in range(tournaments):
            for m in range(matches):
                while self.is_over() == IN_PROG:
                    if self.turn == _X_:
                        self.board[self.pos_1d_to_2d(q_player.make_move(self))] = _X_
                        self.turn = _O_
                    else:
                        self.board[self.pos_1d_to_2d(o_player.make_move(self))] = _O_
                        self.turn = _X_
                #
                # One match is over. Notify players. QPlayer is supposed to update its table now.
                # Each player must keep track of it's own moves.
                self.match_results[t, m] = self.is_over()  # Redundant call. Need to reduce.
                q_player.match_over(self.match_results[t, m])
                o_player.match_over(self.match_results[t, m])
                prev_winner = self.match_results[t, m]
                self.reset(prev_winner)  # prev winner would take first turn
                q_player.next_match()
                o_player.next_match()

            # One tournament is done
            print("****** Tournament:", t, "result", "******", "\n")
            x_wins = np.count_nonzero(self.match_results[t, :] == WIN_X)
            o_wins = np.count_nonzero(self.match_results[t, :] == WIN_O)
            draws = matches - (x_wins + o_wins)
            print("X wins % =", (x_wins / matches) * 100, "O wins % =", (o_wins / matches) * 100, "Draws % =",
                  (draws / matches) * 100, "\n")
        q_player.save_table()

    def board_to_hash(self):
        # str(boardObj.board) : it's easier but string consumes much more memory
        return hash(tuple(map(tuple, self.board)))

    def is_move_valid(self, move: int):
        """
        Checks if the passed move (in 1D) is valid or not. Must first convert 'move' -- which represents
        cell number of board as per row major order -- to 2d (row,col) format
        returns True if valid, else False
        """
        pos = self.pos_1d_to_2d(move)
        # print("is_move_valid", move, pos, self.board[pos])
        if self.board[pos] == _EMPTY_ and (0 <= move < NUM_CELLS):
            return True
        else:
            return False

    def get_empty_cells_1d(self):
        """Returns empty cell positions in 1D format"""
        board_1d = self.board.flatten()
        return np.where(board_1d == _EMPTY_)[0]

    def pos_1d_to_2d(self, pos: int):
        return (pos // BOARD_DIM[1], pos % BOARD_DIM[1])

