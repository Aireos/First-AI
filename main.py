import pygame
import sys
import math

# ======================
# Deterministic PRNG
# ======================

class PRNG:
    def __init__(self, seed=1234):
        self.state = seed

    def next(self):
        self.state = (1664525 * self.state + 1013904223) % (2**32)
        return self.state

    def random(self):
        return self.next() / (2**32)


# ======================
# Environment
# ======================

class ParkourEnv:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.reset()

    def reset(self):
        self.player_x = 100
        self.player_y = 300
        self.vel_y = 0
        self.on_ground = True
        self.done = False

        self.speed = 2 + self.difficulty
        self.obstacles = []

        count = 1 if self.difficulty < 3 else 2

        for i in range(count):
            self.obstacles.append(600 + i * 300)

        return self.get_state()

    def get_state(self):
        nearest = min(self.obstacles)
        distance = nearest - self.player_x
        bucket = max(0, min(15, distance // 40))
        return (bucket, int(self.on_ground))

    def step(self, action):
        reward = 0

        # ACTIONS:
        # 0 = do nothing
        # 1 = move forward
        # 2 = jump

        if action == 1:
            self.player_x += 5

        if action == 2 and self.on_ground:
            self.vel_y = -12
            self.on_ground = False

        # Gravity
        self.vel_y += 0.6
        self.player_y += self.vel_y

        if self.player_y >= 300:
            self.player_y = 300
            self.vel_y = 0
            self.on_ground = True

        # Move obstacles toward player
        for i in range(len(self.obstacles)):
            self.obstacles[i] -= self.speed

        # Check collisions
        for obs in self.obstacles:
            if abs(self.player_x - obs) < 25 and self.player_y > 270:
                reward = -100
                self.done = True

        # Win if all obstacles passed
        if all(obs < 0 for obs in self.obstacles):
            reward = 200
            self.done = True

        reward += 1  # small survival reward

        return self.get_state(), reward, self.done


# ======================
# Agent
# ======================

class Agent:
    def __init__(self):
        self.q = {}
        self.alpha = 0.1
        self.gamma = 0.95
        self.epsilon = 1.0
        self.min_epsilon = 0.05
        self.decay = 0.995
        self.rng = PRNG(999)

    def get_q(self, state, action):
        return self.q.get((state, action), 0.0)

    def choose_action(self, state):
        if self.rng.random() < self.epsilon:
            return int(self.rng.random() * 3)
        else:
            qvals = [self.get_q(state, a) for a in range(3)]
            return qvals.index(max(qvals))

    def update(self, state, action, reward, next_state):
        best_next = max(self.get_q(next_state, a) for a in range(3))
        current = self.get_q(state, action)
        self.q[(state, action)] = current + self.alpha * (
            reward + self.gamma * best_next - current
        )

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon,
                           self.epsilon * self.decay)


# ======================
# Main Loop
# ======================

pygame.init()
screen = pygame.display.set_mode((900, 400))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

agent = Agent()

difficulty = 1
episodes = 0
success_counter = 0

while True:
    env = ParkourEnv(difficulty)
    state = env.reset()
    done = False

    while not done:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)
        agent.update(state, action, reward, next_state)
        state = next_state

        # DRAW
        screen.fill((20, 20, 30))

        pygame.draw.rect(screen, (60, 60, 60), (0, 330, 900, 70))

        for obs in env.obstacles:
            pygame.draw.rect(screen, (200, 50, 50),
                             (obs, 280, 30, 50))

        pygame.draw.rect(screen, (50, 200, 50),
                         (env.player_x, env.player_y, 25, 25))

        text = font.render(
            f"Episode: {episodes}  Level: {difficulty}  Epsilon: {round(agent.epsilon,2)}",
            True, (255, 255, 255)
        )
        screen.blit(text, (10, 10))

        pygame.display.flip()

    # Curriculum logic
    if reward > 0:
        success_counter += 1
    else:
        success_counter = 0

    if success_counter >= 5:
        difficulty += 1
        success_counter = 0
        print("Level Up! Now difficulty:", difficulty)

    agent.decay_epsilon()
    episodes += 1

    if episodes % 50 == 0:
        print("Episode:", episodes,
              "Difficulty:", difficulty,
              "Epsilon:", round(agent.epsilon, 2))