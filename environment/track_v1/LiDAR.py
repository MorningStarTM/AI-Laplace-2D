import pygame
import math


class LiDAR:
    def __init__(self, car_position, car_angle, num_rays=36, max_range=200, visualize=False):
        self.car_position = car_position
        self.car_angle = car_angle
        self.num_rays = num_rays
        self.max_range = max_range
        self.visualize = visualize

    def cast_rays(self, obstacles):
        ray_angles = [self.car_angle + math.radians(angle) for angle in range(-90, 91, 180 // (self.num_rays - 1))]

        distances = []
        for angle in ray_angles:
            for distance in range(self.max_range):
                end_x = self.car_position[0] + distance * math.cos(angle)
                end_y = self.car_position[1] - distance * math.sin(angle)  # Pygame y-axis is flipped
                ray_end = pygame.Vector2(end_x, end_y)

                collision = False
                for obstacle in obstacles:
                    if obstacle.collidepoint(ray_end):
                        distances.append(distance)
                        collision = True
                        break
                if collision:
                    break
            if not collision:
                distances.append(self.max_range)

        return distances

    def draw(self, screen, obstacles):
        if self.visualize:
            # Draw LiDAR rays (optional for visualization)
            ray_angles = [self.car_angle + math.radians(angle) for angle in range(-90, 91, 180 // (self.num_rays - 1))]
            lidar_distances = self.cast_rays(obstacles)

            for i, distance in enumerate(lidar_distances):
                angle = self.car_angle + math.radians(-90 + i * (180 // (self.num_rays - 1)))
                end_x = self.car_position[0] + distance * math.cos(angle)
                end_y = self.car_position[1] - distance * math.sin(angle)  # Pygame y-axis is flipped
                pygame.draw.line(screen, (255, 0, 0), self.car_position, (end_x, end_y))

