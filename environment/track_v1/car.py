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
        self.START_POS = (250, 350)  # Default start position, to be set later
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
        self.vel *= 0.5  # Reduce speed by 50%
        self.collision_timer = 60  # Apply effect for 1 second (assuming 60 FPS)

        # Simple boost for the other car
        other_car.vel = min(other_car.vel + 1, other_car.max_vel)
        other_car.collision_timer = 60

        # Determine collision impact direction
        angle_diff = (self.angle - other_car.angle) % 360
        if 45 < angle_diff < 135 or 225 < angle_diff < 315:
            # Collision from the side
            self.vel = 0
            other_car.vel = 0  

    def get_speed(self):
        return self.vel




class ComputerCar(AbstractCar):
    def __init__(self, img_path, max_vel, rotation_vel):
        super().__init__(img_path, max_vel, rotation_vel)
        self.img = pygame.image.load(img_path)
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.START_POS = (150, 350)  # Default start position, to be set later
        self.x, self.y = self.START_POS
        self.acceration = 0.1
