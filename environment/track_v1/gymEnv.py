import gym
from gym import spaces
import pygame
import numpy as np
from car import AbstractCar, ComputerCar
from track import RaceTrack


class CarRaceEnv(gym.Env):
    """
    Custom Environment for Car Racing.
    This environment uses Pygame for rendering and simulating the car race.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(CarRaceEnv, self).__init__()

        # Define action and observation space
        self.action_space = spaces.Discrete(5)  # 0: No action, 1: Rotate left, 2: Rotate right, 3: Move forward, 4: Move backward

        # Observation space is a vector with position (x, y), angle, and speed
        self.observation_space = spaces.Box(low=np.array([-np.inf, -np.inf, -360, 0]),
                                            high=np.array([np.inf, np.inf, 360, 10]),
                                            dtype=np.float32)

        # Initialize Pygame and create the environment
        pygame.init()
        self.width, self.height = 1250, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Car Racing Environment')

        # Create Track and Car instances
        self.track = RaceTrack(self.width, self.height, 1000, 700, 220, {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'GRAY': (128, 128, 128),
            'GREEN': (0, 255, 0)
        })
        self.car = AbstractCar(img_path="assets/BlueStrip_1.png", max_vel=5, rotation_vel=4)
        self.car.x, self.car.y = 250, 290

        self.clock = pygame.time.Clock()


    