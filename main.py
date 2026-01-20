#AKA learning Q-Learning
import random
import numpy as np

"""
The enviorment needs to have the following:
2d simulation engine
charecter that can move left, right, or up
some basic parkour maps that need to have a spawn, death, and finish
easy inputs and exputs
"""
"""
The checker needs to be able to:
see the distance from the goal/flag the charecter is
check what the distance was last time
based on those two things make a reward that is positive, negitive, or neutral for the model.
"""
"""
the model needs to be able to:
make inputs for the enviorment
take in the outputs of the enviorment
use the checker reward to affect learning
use the following main points:
aplha = learning rate = # between 0-1 that determines to what extent new info (rewards) effect old/current info.
in a deterministice enviorment, 1 is best, but usally use 0.9 for the most part
gamma = discount factor = # between 0-1 about how important future rewards are compared to current
1 means future is same imporantancy as current
0 means current is more imporant then future
epsilon = randomness/exploration rate = # between 0-1
1 = completly random
0 = completley strict to Q-table
should start at one, and as Q-table grows, slowley get more relient on Q-table
eplsilon_decay = # between 0-1, is multiplied by the epsilon to get more relient on the Q-table. 
good number for this is 0.9995
min_eplislon = # between 0-1, is the minumum epislon, so that there always is at least a little bit of randomness for the model
number used in tutorial for this is 0.01
num_episodes = # from 1-infinity, is the number of trials that the program runs
number used in tutorial  for this is 10,000
max_steps = # from 1-infinity, is the max number of actions that the model can do in any given trial
number used in tutorial for this is 100
Q-table = nump array initialized full of 0's = all possible states in the given enviorment
calculated by all factors combined, for the example given from the tutorial:
5x5 grid = 25 posisitions * 5 possible person spaces * 4 possible hotel spaces = 500 possible states
each of these states can have 4 actions (techinicly the edges have less, but oh well) (actually, they would have an action, it just wouldn't do anything)
here is gemeni's explanation for it: 
The Q-table is a matrix where rows represent all possible states and columns represent all possible actions
needs more expaining.
"""
