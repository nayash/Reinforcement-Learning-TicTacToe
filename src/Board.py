#
# Copyright (c) 2019. Asutosh Nayak (nayak.asutosh@ymail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#

import pickle
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = r'your_path_to_ffmpeg_bin\ffmpeg.exe'
from matplotlib import animation

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

OUTPUT_PATH = ".\\output\\"
OUTPUT_FILE_NAME = "anim_data.pickle"

class Board:
    """
    This represents the board on which Tic-Tac-Toe is played.
    It includes the current state of the board instance and methods to
    enforce game rules.
    """

    def __init__(self, turn=_X_, is_visual_enabled=True):
        self.board = np.full((3, 3), _EMPTY_)
        self.turn = turn
        self.tournaments_stat = []
        self.init_pyplot()
        self.is_visual_enabled = is_visual_enabled

    def init_pyplot(self):
        self.anim_frame_data = []  # (player, move) or (player, ): denotes 'player' won or (): reset plot
        self.fig = plt.figure(num=None, figsize=(5, 5))
        plt.title("Tic Tac Toe")
        # plt.axis('off')
        plt.tight_layout(2)

    def plot_layout(self):
        plt.clf()
        # draw horizontal lines
        plt.plot([0, 2, 4, 6], [0, 0, 0, 0], 'b-')
        plt.plot([0, 2, 4, 6], [2, 2, 2, 2], 'b-')
        plt.plot([0, 2, 4, 6], [4, 4, 4, 4], 'b-')
        plt.plot([0, 2, 4, 6], [6, 6, 6, 6], 'b-')
        # draw vertical lines
        plt.plot([0, 0, 0, 0], [0, 2, 4, 6], 'b-')
        plt.plot([2, 2, 2, 2], [0, 2, 4, 6], 'b-')
        plt.plot([4, 4, 4, 4], [0, 2, 4, 6], 'b-')
        plt.plot([6, 6, 6, 6], [0, 2, 4, 6], 'b-')

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

        print("Starting Game...")
        self.match_results = np.full((tournaments, matches), -1)
        save_4_anim = False
        for t in range(tournaments):
            for m in range(matches):
                if (t == tournaments-1 and matches-m <= 5) or (t == 0 and m < 5):
                    # save first 5 and last 5 games to show visuals
                    save_4_anim = True
                else:
                    save_4_anim = False

                while self.is_over() == IN_PROG:
                    if self.turn == _X_:
                        pos = self.pos_1d_to_2d(q_player.make_move(self))
                        self.board[pos] = _X_
                        self.turn = _O_
                        if save_4_anim:
                            self.anim_frame_data.append((_X_, pos))
                    else:
                        pos = self.pos_1d_to_2d(o_player.make_move(self))
                        self.board[pos] = _O_
                        self.turn = _X_
                        if save_4_anim:
                            self.anim_frame_data.append((_O_, pos))
                #
                # One match is over. Notify players. QPlayer is supposed to update its table now.
                # Each player must keep track of it's own moves.
                self.match_results[t, m] = self.is_over()  # Redundant call. Need to reduce.
                q_player.match_over(self.match_results[t, m])
                o_player.match_over(self.match_results[t, m])
                prev_winner = self.match_results[t, m]
                if save_4_anim:
                    self.anim_frame_data.append((prev_winner, ))
                self.reset(prev_winner)  # prev winner would take first turn
                if save_4_anim:
                    self.anim_frame_data.append(())
                q_player.next_match()
                o_player.next_match()

            # One tournament is done
            print("****** Tournament:", t, "result", "******", "\n")
            x_wins = np.count_nonzero(self.match_results[t, :] == WIN_X)
            o_wins = np.count_nonzero(self.match_results[t, :] == WIN_O)
            draws = matches - (x_wins + o_wins)
            print("X wins % =", (x_wins / matches) * 100, "O wins % =", (o_wins / matches) * 100, "Draws % =",
                  (draws / matches) * 100, "\n")
        q_player.save_data()
        o_player.save_data()
        print("Anim data len", len(self.anim_frame_data))
        self.save_anim_data()
        if self.is_visual_enabled:
            self.start_visual()

    def save_anim_data(self):
        pickle.dump(self.anim_frame_data, open(OUTPUT_PATH + OUTPUT_FILE_NAME, "wb"))
        print("Animation data saved")

    def load_anim_data(self):
        self.anim_frame_data = pickle.load(open(OUTPUT_PATH+OUTPUT_FILE_NAME, 'rb'))
        print("Animation data loaded")

    def start_visual(self):
        import sys
        anim = animation.FuncAnimation(fig=self.fig, func=self.animate, frames=self.anim_frame_data, init_func=self.plot_layout,
                                       interval=1000, repeat=False, save_count=sys.maxsize)
        plt.show()
        self.save_animation_video(anim)

    def save_animation_video(self, anim):
        # Writer = animation.writers['ffmpeg']
        ff_writer = animation.FFMpegWriter(fps=1, metadata=dict(title='Reinforcement Learning', artist='Asutosh Nayak',
                                                                copyright='Rights Reserved'), extra_args=['-vcodec', 'libx264'])
        # writer = Writer(fps=1, metadata=dict(artist='Asutosh Nayak'), bitrate=1800)
        anim.save(OUTPUT_PATH+"training_games.mp4", writer=ff_writer)
        print("Animation saved as video file")

    def animate(self, curr_move):
        if len(curr_move) == 1:
            if curr_move[0] == _X_:
                plt.xlabel("Player X (Q-Player) won")
            elif curr_move[0] == _O_:
                plt.xlabel("Player O (MinMax Player) won")
            else:
                plt.xlabel("Game draw")
        elif len(curr_move) == 0:
            plt.xlabel("Reset for new game")
            self.plot_layout()
        else:
            plt.xlabel("Game in progress")
            symbol = "-"
            color = "-"
            if curr_move[0] == _X_:
                symbol = "X"
                color = 'g'
            else:
                symbol = "O"
                color = 'r'
            plot_pos = self.mat_pos_to_plot_pos(curr_move[1])
            plt.text(plot_pos[0], plot_pos[1], symbol, fontsize=25, horizontalalignment='center', verticalalignment='center', color=color,
                     fontweight='bold')

    def mat_pos_to_plot_pos(self, mat_pos):
        return 2*mat_pos[0] + 1, (6 - (2*mat_pos[1] + 1))

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

