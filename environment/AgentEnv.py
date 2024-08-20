import pygame
import numpy as np
from .track_v1 import AbstractCar, RaceTrack
import sys
import time
import math


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

def euclidean_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.

    :param point1: Tuple (x1, y1) representing the coordinates of the first point.
    :param point2: Tuple (x2, y2) representing the coordinates of the second point.
    :return: Euclidean distance between the two points.
    """
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

class RaceEnv:
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
        #pygame.init()
        self.width, self.height = 1250, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        #pygame.display.set_caption('Car Racing Environment')

        # Create Track and Car instances
        self.track = RaceTrack(self.width, self.height, 1000, 700, 220, COLORS)
        self.car = AbstractCar(img_path="environment\\track_v1\\assets\\BlueStrip_1.png", max_vel=2.5, rotation_vel=3.1)
        self.car.x, self.car.y = 250, 290

        self.clock = pygame.time.Clock()
        self.frame_iteration = 0  
        self.point = [(600, 50), (905, 400), (600, 530)]
        self.track_point = [(128, 200),(960, 50),(900, 590),(300, 530), (100, 380)]
        self.total_distance = 0 
        self.point_a = False
        self.point_b = False
        self.point_c = False

        self.point_1 = False
        self.point_2 = False
        self.point_3 = False
        self.point_4 = False
        self.point_5 = False

    def reset(self):
        self.car = AbstractCar(img_path="environment\\track_v1\\assets\\BlueStrip_1.png", max_vel=5, rotation_vel=4)
        self.car.x, self.car.y = 250, 290
        self.frame_iteration = 0 
        self.total_distance = 0
        return self._get_observation()
         
    def step(self, action):
        
        done = False
        

        reward = 0
        self.car.move_forward()
        # Define action effects
        if action == 0:  # Rotate left
            self.car.rotate(left=True)
        elif action == 1:  # Rotate right
            self.car.rotate(right=True)
        #elif action == 2:  # Move forward
        #    self.car.move_forward()
        #elif action == 4:  # Move backward
        #    self.car.move_backward()

        # Update car position
        self.car.move()

        self.frame_iteration += 1

        if self.track.point_A_line_collide(self.car):
            self.point_a = True
            reward = 0.05

        if self.track.point_B_line_collide(self.car):
            self.point_b = True
            reward = 0.1
            
        if self.track.point_C_line_collide(self.car):
            self.point_c = True
            reward = 0.8

        if self.track.point_line_collide(pos=self.track_point[0], size=(220, 2), car=self.car):
            self.point_1 = True
        if self.track.point_line_collide(pos=self.track_point[1], size=(2, 220), car=self.car):
            self.point_2 = True
        if self.track.point_line_collide(pos=self.track_point[2], size=(220, 2), car=self.car):
            self.point_3 = True
        if self.track.point_line_collide(pos=self.track_point[3], size=(2, 220), car=self.car):
            self.point_4 = True  

        if not self.point_1:
            self.total_distance = euclidean_distance(point1=self.car.get_position(), point2=self.track_point[0]) + euclidean_distance(point1=self.track_point[0], point2=self.track_point[1]) + euclidean_distance(point1=self.track_point[1], point2=self.track_point[2]) + euclidean_distance(point1=self.track_point[2], point2=self.track_point[3]) + euclidean_distance(point1=self.track_point[3], point2=self.track_point[4])
            #print(f"{euclidean_distance(point1=car.get_position(), point2=track_point[0])} + {euclidean_distance(point1=track_point[0], point2=track_point[1])} = {euclidean_distance(point1=car.get_position(), point2=track_point[0]) + euclidean_distance(point1=track_point[0], point2=track_point[1])}")
        
        if self.point_1 and not self.point_2:
            self.total_distance = euclidean_distance(point1=self.car.get_position(), point2=self.track_point[1]) + euclidean_distance(point1=self.track_point[1], point2=self.track_point[2]) + euclidean_distance(point1=self.track_point[2], point2=self.track_point[3]) + euclidean_distance(point1=self.track_point[3], point2=self.track_point[4])
         
        if self.point_1 and self.point_2 and not self.point_3:
            self.total_distance = euclidean_distance(point1=self.car.get_position(), point2=self.track_point[2]) + euclidean_distance(point1=self.track_point[2], point2=self.track_point[3]) + euclidean_distance(point1=self.track_point[3], point2=self.track_point[4])

        if self.point_1 and self.point_2 and self.point_3 and not self.point_4:
            self.total_distance = euclidean_distance(point1=self.car.get_position(), point2=self.track_point[3]) + euclidean_distance(point1=self.track_point[3], point2=self.track_point[4])
        
        if self.point_1 and self.point_2 and self.point_3 and self.point_4 and not self.point_5:
            self.total_distance = euclidean_distance(point1=self.car.get_position(), point2=self.track_point[4])

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

        elif self.frame_iteration % 600 == 0:  # Check if frame iteration limit is exceeded
            reward = -0.01  # Assign negative reward for exceeding the frame iteration limit
            done = False
        else:
            reward = 0.01
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





