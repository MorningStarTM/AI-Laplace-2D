import pygame
import numpy as np
from track_v1 import AbstractCar, RaceTrack
import sys
import time

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


class CarRaceEnv:
    """
    Custom Environment for Car Racing without Gym.
    This environment uses Pygame for rendering and simulating the car race.
    """
    
    def __init__(self):
        # Define action and observation space
        self.action_space = 4  # 0: No action, 1: Rotate left, 2: Rotate right, 3: Move forward, 4: Move backward

        # Observation space is a vector with position (x, y), angle, and speed
        self.observation_space = np.array([-np.inf, -np.inf, 0, 0, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf],
                                          dtype=np.float32)

        # Create RaceTrack instance
        self.track = RaceTrack(WIDTH, HEIGHT, OUTER_TRACK_WIDTH, OUTER_TRACK_HEIGHT, TRACK_THICKNESS, COLORS)

        # Initialize Pygame and create the environment
        pygame.init()
        self.width, self.height = 1250, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Car Racing Environment')

        # Create Track and Car instances
        self.track = RaceTrack(self.width, self.height, 1000, 700, 220, COLORS)
        self.car = AbstractCar(img_path="track_v1\\assets\\BlueStrip_1.png", max_vel=5, rotation_vel=4)
        self.car.x, self.car.y = 250, 290

        self.clock = pygame.time.Clock()
        self.frame_iteration = 0  

    def reset(self):
        self.car = AbstractCar(img_path="track_v1\\assets\\BlueStrip_1.png", max_vel=5, rotation_vel=4)
        self.car.x, self.car.y = 250, 290
        self.frame_iteration = 0 
        return self._get_observation()
         
    def step(self, action):
        done = False
        reward = 0
        # Define action effects
        if action == 1:  # Rotate left
            self.car.rotate(left=True)
        elif action == 2:  # Rotate right
            self.car.rotate(right=True)
        elif action == 3:  # Move forward
            self.car.move_forward()
        #elif action == 4:  # Move backward
        #    self.car.move_backward()

        # Update car position
        self.car.move()

        self.frame_iteration += 1  

        if self.track.start_line_collide(self.car):
            done = False
            self.car.bounce()

        # Check collision with finish line
        if self.track.finish_line_collide(self.car):
            reward = 100.0  # Reward for finishing line collision
            done = True

        elif self.car.collide(self.track):
            self.car.bounce()
            reward = -1.0  # Negative reward for collision with the track
            done = False

        elif self.frame_iteration > 400:  # Check if frame iteration limit is exceeded
            reward = -10.0  # Assign negative reward for exceeding the frame iteration limit
            done = True
        else:
            reward = -0.1
            done = False

        return self._get_observation(), reward, done, self.frame_iteration
    
    def render(self):
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




def main():
    # Initialize the environment
    env = CarRaceEnv()
    
    # Reset the environment to the initial state
    observation = env.reset()

    # Sample actions (for demonstration purposes)
    actions = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]  # Rotate left, Rotate right, Move forward
    
    try:
        for action in actions:
            # Step through the environment with the sample action
            observation, reward, done, frame_iteration = env.step(action)
            
            # Render the environment
            env.render()
            
            # Print out the current state and reward for observation
            print(f"Action: {action}, Reward: {reward}, Done: {done}")
            
            # Pause for a short period to visualize the changes
           

            if done:
                print("Episode finished.")
                break

    finally:
        # Close the environment and Pygame
        env.close()

if __name__ == "__main__":
    main()
