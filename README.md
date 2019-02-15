# Reinforcement-Learning-TicTacToe
Project to demonstrate how Reinforncement Learning or more specifically Q-Learning can be used to make a program learn from the environment.

QPlayer (the target Q-Learning player) can be trained with either a random move making player (OtherPlayer) or MinMaxPlayer (implementation of MiniMax algorithm). MinMaxPlayer caches calculated values which significantly improves computation time (We have to suffer for a first few moves though).

Once the training is done, you can see how the program learned from it's past experiences with animations or save it as video for later.

Note: Since MiniMax would always choose the best move, the best our player can do is tie/draw the game.

Current Limitations (What I have found till now): 1. Since MiniMax is a deterministic algorithm it always produces the same output for a given game state. Hence after certain iterations, the Q-Player ends up seeing same board state and learning same values. Random player can be mixed in the training. Need to randomize the MiniMax algorithm somehow! 

Watch the program in action https://github.com/DarkKnight1991/Reinforcement-Learning-TicTacToe/blob/master/src/output/training_games_trimmed.mp4
