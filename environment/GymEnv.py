import gym
from gym import spaces
import pygame
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
    Custom Environment for Car Racing.
    This environment uses Pygame for rendering and simulating the car race.
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

        # Create Track and Car instances
        self.track = RaceTrack(self.width, self.height, 1000, 700, 220, {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'GRAY': (128, 128, 128),
            'GREEN': (0, 255, 0)
        })
        self.car = AbstractCar(img_path="track_v1\\assets\\BlueStrip_1.png", max_vel=5, rotation_vel=4)
        self.car.x, self.car.y = 250, 290

        self.clock = pygame.time.Clock()


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

        # Check collision with finish line
        if self.track.finish_line_collide(self.car):
            reward = 1.0  # Reward for finishing line collision
            done = True
        elif self.car.collide(self.track):
            reward = -1.0  # Negative reward for collision with the track
            done = True
        else:
            reward = 0.0
            done = False

        return self._get_observation(), reward, done, {}
    

    def render(self, mode='human'):
        if mode == 'human':
            self.screen.fill((255, 255, 255))  # Clear screen
            self.track.draw(self.screen)
            self.car.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)  # Cap the frame rate

    def close(self):
        pygame.quit()
        sys.exit()

    
    def _get_observation(self):
        # Return the current state as observation
        pos = self.car.get_position()
        angle = self.car.get_angle()
        speed = self.car.get_speed()
        orientation = self.car.get_orientation()
        velocity = self.car.get_velocity()
        steer_angle = self.car.get_steering_angle()
        obs_dis = self.car.get_distances_to_obstacles(self.track)
        return np.array([pos[0], pos[1], angle, speed, orientation, velocity, steer_angle, obs_dis[0], obs_dis[1], obs_dis[2], obs_dis[3], \
                         obs_dis[4], obs_dis[5], obs_dis[6], obs_dis[7]], dtype=np.float32)