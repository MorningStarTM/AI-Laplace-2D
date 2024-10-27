# main.py

import gym
import numpy as np
from gym import spaces
import pygame
from car import AbstractCar, ComputerCar
from track import RaceTrack


WIDTH, HEIGHT = 1250, 800
OUTER_TRACK_WIDTH = 1000
OUTER_TRACK_HEIGHT = 700
TRACK_THICKNESS = 220

COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128),
    'GREEN': (0, 255, 0)
}

class RaceCarEnv(gym.Env):
    def __init__(self, car_image_path, screen_width=1000, screen_height=700):
        super(RaceCarEnv, self).__init__()

        # Initialize Pygame and create screen
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Define action and observation spaces
        self.action_space = spaces.Box(low=np.array([-1.0, -1.0]), high=np.array([1.0, 1.0]), dtype=np.float32)
        self.observation_space = spaces.Box(low=0, high=255, shape=(WIDTH, HEIGHT, 3), dtype=np.uint8)

        # Load car and track
        self.car = AbstractCar(car_image_path, max_vel=2, rotation_vel=5)
        self.track = RaceTrack(WIDTH, HEIGHT, OUTER_TRACK_WIDTH, OUTER_TRACK_HEIGHT, TRACK_THICKNESS, COLORS)

    def reset(self):
        # Reset car to starting position and velocity
        self.car.x, self.car.y = self.car.START_POS
        self.car.angle = 0
        self.car.vel = 0

        # Return initial observation (screen)
        observation = self.render()
        return observation

    def step(self, action):
        # Apply action to car
        self.car.step(action)

        # Check for collisions with track
        done = False
        reward = 0.0
        if self.track.finish_line_collide(self.car):
            reward = 100.0  # Reward for crossing the finish line
            done = False
        elif self.car.collide(self.track):
            reward = -100.0  # Penalty for colliding with track boundary
            done = False
        else:
            reward = 0.1 * self.car.get_velocity()  # Reward proportional to speed

        # Return observation, reward, done, info
        observation = self.render()
        info = {}
        return observation, reward, done, info

    def render(self, mode='rgb_array'):
        # Clear the screen
        self.screen.fill((255, 255, 255))

        # Draw track and car
        self.track.draw(self.screen)
        self.car.draw(self.screen)

        # Update display
        pygame.display.flip()

        # Convert Pygame surface to numpy array for Gym
        return np.array(pygame.surfarray.array3d(self.screen))

    def close(self):
        pygame.quit()

# Run environment with random actions for testing
if __name__ == "__main__":
    env = RaceCarEnv(car_image_path="assets\\BlueStrip_1.png")
    obs = env.reset()

    for _ in range(1000):
        # Generate a random action (acceleration, steering angle)
        action = env.action_space.sample()
        
        # Step the environment
        obs, reward, done, info = env.step(action)

        # Print reward and check if episode ended
        print(f"Reward: {reward}")
        if done:
            print("Episode finished!")
            break
    
    env.close()
