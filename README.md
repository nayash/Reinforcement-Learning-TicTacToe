# Reinforcement-Learning-TicTacToe
Project to demonstrate how Reinforncement Learning or more specifically Q-Learning can be used to make a program learn from the environment.

QPlayer (the target Q-Learning player) can be trained with either a random move making player (RandomPlayer) or MinMaxPlayer (implementation of MiniMax algorithm). MinMaxPlayer caches calculated values which significantly improves computation time (We have to suffer for a first few moves though).

Once the training is done, you can see how the program learned from it's past experiences with animations or save it as video for later.
Right now video & animation show only first 5 and last 5 training games, not all.

Note: Since MiniMax would always choose the best move, the best our player can do is tie/draw the game.

Current Limitations (What I have found till now)
1. Since MiniMax is a deterministic algorithm it always produces the same output for a given game state. Hence after certain iterations, the Q-Player ends up seeing same board state and learning same values. Random player can be mixed in the training. Need to randomize the MiniMax algorithm somehow! We can also train the player with a mix of opponents for eg. train with MinMaxPlayer then load the learning data using load_data function and then continue training with OtherPlayer (random player). 

UPDATE: Added a new player strategy -pseudo random- which uses MiniMax and random strategy altenately to mimic human errors and hence help the Qplayer see more number of board states. So above limitation is overcome to some extent.

Watch the program in action https://github.com/DarkKnight1991/Reinforcement-Learning-TicTacToe/blob/master/src/output/training_games_trimmed.mp4

![alt text](https://github.com/DarkKnight1991/Reinforcement-Learning-TicTacToe/blob/master/src/output/training_games_trimmed.mp4)

# How to run it
Just open the Main.py file, initialize  "o_player" to the player object that you want to play with and let the magic begin.
