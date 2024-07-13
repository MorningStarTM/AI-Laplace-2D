import pygame
import math
from lidar import LiDAR


def scale(img, factor):
    size = round(img.get_width() * (factor + 0.7)), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def scale_car(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * (factor - 0.2))
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center
    )
    win.blit(rotated_image, new_rect.topleft)


class AbstractCar:
    """
    Base class for Car
    """

    def __init__(self, img_path, max_vel, rotation_vel):
        self.img = pygame.image.load(img_path)
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0  # Initial angle set to 0
        self.START_POS = (250, 380)  # Default start position, to be set later
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.lidar = LiDAR((self.x, self.y), self.acceleration, self.max_vel, self.angle)

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
        self.update_lidar()

    def draw(self, win, obstacles):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
        self.lidar.draw(win, obstacles)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
        self.update_lidar()

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
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
        rotated_image = pygame.transform.rotate(self.img, self.angle)
        return pygame.mask.from_surface(rotated_image)

    def car_collide(self, other_car):
        offset = (int(other_car.x - self.x), int(other_car.y - self.y))
        overlap = self.get_mask().overlap(other_car.get_mask(), offset)
        return overlap is not None

    def apply_collision_effect(self, other_car):
        impact_force = self.vel * 0.5
        self.vel *= 0.5  # Reduce speed by 50%
        other_car.vel = min(other_car.vel + impact_force, other_car.max_vel)

        collision_angle = math.atan2(self.y - other_car.y, self.x - other_car.x)
        self_angle_radians = math.radians(self.angle)
        other_angle_radians = math.radians(other_car.angle)

        self.vel -= math.cos(self_angle_radians - collision_angle) * impact_force
        other_car.vel += math.cos(other_angle_radians - collision_angle) * impact_force

        self.x -= math.cos(collision_angle) * impact_force
        self.y -= math.sin(collision_angle) * impact_force
        other_car.x += math.cos(collision_angle) * impact_force
        other_car.y += math.sin(collision_angle) * impact_force

        self.collision_timer = 60
        other_car.collision_timer = 60

    def update_lidar(self):
        self.lidar.car_position = (self.x+30, self.y+20)
        self.lidar.car_angle = math.radians(self.angle+1.57)

    def get_speed(self):
        return self.vel

    def get_angle(self):
        return self.angle
    


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
        self.acceleration = 0.1
