#AKA learning Q-Learning
import random
import numpy as np
import pygame
import sys
"""
The enviorment needs to have the following:
2d simulation engine
charecter that can move left, right, or up
some basic parkour maps that need to have a spawn, block, death, and finish
easy inputs and exputs
"""
"""
The checker needs to be able to:
see the distance from the goal/flag the charecter is
check what the distance was last time
based on those two things make a reward that is positive or negitive for the model.
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
"""
the runner needs to be able to open a pygame window and show relevenent info and controls while showing the current running program such as:
current episode / total episodes
be able to view multiple episode saved history running at once
stop current episode
continue current episode
save current ai
current fitness / eplisolon
exit
"""

#example program made by gemini:

import pygame
import numpy as np
import random
import sys

# --- CONFIGURATION ---
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 40
COLS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
ALPHA, GAMMA = 0.9, 0.95
EPSILON, EPS_DECAY, MIN_EPS = 1.0, 0.9995, 0.01
NUM_EPISODES, MAX_STEPS = 10000, 100

# Map: 0=Empty, 1=Wall, 2=Spawn, 3=Finish, 4=Death
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,0,0,0,1,0,0,0,0,0,0,0,3,1],
    [1,0,0,4,0,1,0,1,1,1,0,4,0,0,1],
    [1,0,1,1,0,0,0,0,0,1,0,1,1,0,1],
    [1,0,0,0,0,4,1,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Environment:
    def __init__(self):
        self.reset()

    def reset(self):
        for r in range(len(MAP)):
            for c in range(len(MAP[0])):
                if MAP[r][c] == 2: self.pos = [r, c]
                if MAP[r][c] == 3: self.goal = [r, c]
        self.last_dist = self.get_dist()
        return self.get_state()

    def get_dist(self):
        return np.sqrt((self.pos[0]-self.goal[0])**2 + (self.pos[1]-self.goal[1])**2)

    def get_state(self):
        return self.pos[0] * len(MAP[0]) + self.pos[1]

    def step(self, action):
        # 0:Up, 1:Down, 2:Left, 3:Right
        move = {0:[-1,0], 1:[1,0], 2:[0,-1], 3:[0,1]}[action]
        new_pos = [self.pos[0]+move[0], self.pos[1]+move[1]]
        
        cell = MAP[new_pos[0]][new_pos[1]]
        reward, done = -1, False # Default step penalty

        if cell != 1: # Move if not wall
            self.pos = new_pos
        
        curr_dist = self.get_dist()
        reward += (self.last_dist - curr_dist) * 2 # Reward for getting closer
        self.last_dist = curr_dist

        if cell == 3: reward, done = 100, True  # Goal
        elif cell == 4: reward, done = -100, True # Death
        
        return self.get_state(), reward, done

class QModel:
    def __init__(self, states, actions):
        self.q_table = np.zeros((states, actions)) #
        self.eps = EPSILON

    def choose_action(self, state):
        if random.uniform(0, 1) < self.eps:
            return random.randint(0, 3) # Explore
        return np.argmax(self.q_table[state]) # Exploit

    def learn(self, s, a, r, s_next):
        old_val = self.q_table[s, a]
        next_max = np.max(self.q_table[s_next])
        # Q-Learning Formula
        self.q_table[s, a] = (1 - ALPHA) * old_val + ALPHA * (r + GAMMA * next_max)
        self.eps = max(MIN_EPS, self.eps * EPS_DECAY)

# --- RUNNER ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))
clock = pygame.time.Clock()
env = Environment()
model = QModel(len(MAP) * len(MAP[0]), 4)

for ep in range(NUM_EPISODES):
    state = env.reset()
    for _ in range(MAX_STEPS):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        action = model.choose_action(state)
        next_state, reward, done = env.step(action)
        model.learn(state, action, reward, next_state)
        state = next_state

        # Rendering
        screen.fill((30, 30, 30))
        for r in range(len(MAP)):
            for c in range(len(MAP[0])):
                color = {0:(50,50,50), 1:(100,100,100), 2:(0,255,0), 3:(255,215,0), 4:(255,0,0)}[MAP[r][c]]
                pygame.draw.rect(screen, color, (c*GRID_SIZE, r*GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2))
        
        pygame.draw.circle(screen, (0,150,255), (env.pos[1]*GRID_SIZE+20, env.pos[0]*GRID_SIZE+20), 15)
        
        # Stats UI
        font = pygame.font.SysFont('Arial', 18)
        txt = font.render(f"Ep: {ep}/{NUM_EPISODES} | Eps: {model.eps:.4f} | Fitness: {reward}", True, (255,255,255))
        screen.blit(txt, (10, HEIGHT + 10))
        
        pygame.display.flip()
        if done: break
