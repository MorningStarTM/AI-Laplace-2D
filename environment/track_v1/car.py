# car.py
import pygame
import math
from utils import blit_rotate_center

class AbstractCar:
    """
    Base class for Car
    """
    def __init__(self, img_path, max_vel, rotation_vel):
        self.img = pygame.image.load(img_path)
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.START_POS = (250, 290)  # Default start position, to be set later
        self.x, self.y = self.START_POS
        self.acceration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceration / 2, 0)
        self.move()

    def get_rect(self):
        car_rect = self.img.get_rect(topleft=(self.x, self.y))
        rotated_rect = pygame.Rect(car_rect)
        rotated_rect.center = car_rect.center
        return rotated_rect

    def collide(self, track):
        outer_track_rect = track.get_outer_track_rect()
        inner_track_rect = track.get_inner_track_rect()

        car_rect = self.get_rect()
        return not outer_track_rect.contains(car_rect) or inner_track_rect.colliderect(car_rect)

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def get_mask(self):
        # Get the mask of the car image for pixel-level collision detection
        rotated_image = pygame.transform.rotate(self.img, self.angle)
        return pygame.mask.from_surface(rotated_image)

    def car_collide(self, other_car):
        # Check for pixel-level collision with another car
        offset = (int(other_car.x - self.x), int(other_car.y - self.y))
        overlap = self.get_mask().overlap(other_car.get_mask(), offset)
        return overlap is not None

    def apply_collision_effect(self, other_car):
        # Calculate the impact force and direction
        impact_force = self.vel * 0.5
        self.vel *= 0.5  # Reduce speed by 50%
        other_car.vel = min(other_car.vel + impact_force, other_car.max_vel)

        # Calculate the angle of collision
        collision_angle = math.atan2(self.y - other_car.y, self.x - other_car.x)
        self_angle_radians = math.radians(self.angle)
        other_angle_radians = math.radians(other_car.angle)

        # Apply forces based on collision angle
        self.vel -= math.cos(self_angle_radians - collision_angle) * impact_force
        other_car.vel += math.cos(other_angle_radians - collision_angle) * impact_force

        # Apply direction adjustment
        self.x -= math.cos(collision_angle) * impact_force
        self.y -= math.sin(collision_angle) * impact_force
        other_car.x += math.cos(collision_angle) * impact_force
        other_car.y += math.sin(collision_angle) * impact_force

        # Reset collision timer
        self.collision_timer = 60
        other_car.collision_timer = 60

    def get_speed(self):
        return self.vel

    def get_angle(self):
        return self.angle

    def get_position(self):
        return (self.x, self.y)

    def get_orientation(self):
        return self.angle % 360

    def get_velocity(self):
        return self.vel

    def get_steering_angle(self):
        return self.angle % 360 # Assuming steering angle is directly related to the car's angle

    def get_distances_to_obstacles(self, track, num_directions=8):
        distances = []
        directions = [i * (360 / num_directions) for i in range(num_directions)]
        for direction in directions:
            angle_rad = math.radians(direction)
            x_step = math.cos(angle_rad)
            y_step = math.sin(angle_rad)
            distance = 0

            while distance < 100:  # Max distance to check
                check_x = self.x + distance * x_step
                check_y = self.y + distance * y_step

                if not track.get_outer_track_rect().collidepoint(check_x, check_y) or track.get_inner_track_rect().collidepoint(check_x, check_y):
                    break

                distance += 1
            distances.append(distance)
        return distances



class ComputerCar(AbstractCar):
    def __init__(self, img_path, max_vel, rotation_vel):
        super().__init__(img_path, max_vel, rotation_vel)
        self.img = pygame.image.load(img_path)
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.START_POS = (150, 290)  # Default start position, to be set later
        self.x, self.y = self.START_POS
        self.acceration = 0.1