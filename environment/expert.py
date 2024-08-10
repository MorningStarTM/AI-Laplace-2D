from gym import spaces
import pygame
import gym
import numpy as np
from track_v1 import AbstractCar, ComputerCar
from track_v1 import RaceTrack
import sys

COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128),
    'GREEN': (0, 255, 0)
}

WIDTH, HEIGHT = 1250, 800
OUTER_TRACK_WIDTH = 1000
OUTER_TRACK_HEIGHT = 700
TRACK_THICKNESS = 220


class CarRaceEnv(gym.Env):
    """
    Custom Environment for Car Racing with manual control and data collection.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(CarRaceEnv, self).__init__()

        # Define action and observation space
        self.action_space = spaces.Discrete(5)  # 0: No action, 1: Rotate left, 2: Rotate right, 3: Move forward, 4: Move backward

        # Observation space is a vector with position (x, y), angle, and speed
        self.observation_space = spaces.Box(low=np.array([-np.inf, -np.inf, 0, 0, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf]),
                                            high=np.array([np.inf, np.inf, 360, 10, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]),
                                            dtype=np.float32)

        # Create RaceTrack instance
        self.track = RaceTrack(WIDTH, HEIGHT, OUTER_TRACK_WIDTH, OUTER_TRACK_HEIGHT, TRACK_THICKNESS, COLORS)

        # Initialize Pygame and create the environment
        pygame.init()
        self.width, self.height = 1250, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Car Racing Environment')

        # Create Car instances
        self.car = AbstractCar(img_path="track_v1\\assets\\BlueStrip_1.png", max_vel=5, rotation_vel=4)
        self.car.x, self.car.y = 250, 290

        self.clock = pygame.time.Clock()

        # Initialize data collection
        self.data = []

    
    def reset(self):
        self.car = AbstractCar(img_path="track_v1\\assets\\BlueStrip_1.png", max_vel=5, rotation_vel=4)
        self.car.x, self.car.y = 250, 290
        return self._get_observation()
    

    def step(self, action):
        # Define action effects
        if action == 1:  # Rotate left
            self.car.rotate(left=True)
        elif action == 2:  # Rotate right
            self.car.rotate(right=True)
        elif action == 3:  # Move forward
            self.car.move_forward()
        elif action == 4:  # Move backward
            self.car.move_backward()

        # Update car position
        self.car.move()

        # Check collision with the track and finishing line
        if self.track.start_line_collide(self.car):
            done = False
            #self.car.bounce()
        if self.track.finish_line_collide(self.car):
            reward = 10.0  # Reward for finishing line collision
            done = True
        elif self.car.collide(self.track):
            reward = -1.0  # Negative reward for collision with the track
            done = False
        else:
            reward = 0.1
            done = False

        next_state = self._get_observation()
        self.data.append((self._get_observation(), action, reward, next_state, done))
        
        if done:
            print("Finished line collided. Data saved.")
            # Do not close the display
        return next_state, reward, done, {}
