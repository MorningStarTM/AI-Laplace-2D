import pygame
import sys
from lidarCar import AbstractCar, ComputerCar
from track import RaceTrack

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1250, 800
OUTER_TRACK_WIDTH = 1000
OUTER_TRACK_HEIGHT = 700
TRACK_THICKNESS = 220

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Simulation with LiDAR")

# Colors
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128),
    'GREEN': (0, 255, 0)
}

# Load car images
CAR_IMAGE = 'assets\\BlueStrip_1.png'  # Replace with your car image path
COMPUTER_CAR_IMAGE = 'assets\\GreenStrip.png'  # Replace with your computer car image path

# Create the race track
TRACK = RaceTrack(WIDTH, HEIGHT, OUTER_TRACK_WIDTH, OUTER_TRACK_HEIGHT, TRACK_THICKNESS, COLORS)

def main():
    clock = pygame.time.Clock()
    run = True

    # Create the player car
    player_car = AbstractCar(CAR_IMAGE, max_vel=4, rotation_vel=5)
    player_car.START_POS = (400, 300)

    # Simple obstacle representation (rectangles)
    obstacles = [
        pygame.Rect(300, 200, 100, 20),
        pygame.Rect(100, 400, 50, 100),
        pygame.Rect(500, 400, 80, 50)
    ]

    while run:
        clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_car.rotate(left=True)
        if keys[pygame.K_d]:
            player_car.rotate(right=True)
        if keys[pygame.K_w]:
            player_car.move_forward()
        if keys[pygame.K_s]:
            player_car.move_backward()
        if keys[pygame.K_v]:
            player_car.lidar.visualize = not player_car.lidar.visualize

        # Draw everything
        WIN.fill(COLORS['WHITE'])
        TRACK.draw(WIN)
        for obstacle in obstacles:
            pygame.draw.rect(WIN, COLORS['BLACK'], obstacle)
        player_car.draw(WIN, obstacles)

        pygame.display.update()

if __name__ == "__main__":
    main()
