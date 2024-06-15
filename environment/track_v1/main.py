import pygame
from track_1 import RaceTrack
from car import AbstractCar
from utils import blit_rotate_center

def main():
    # Initialize Pygame
    pygame.init()

    # Game settings
    WIDTH, HEIGHT = 1250, 800
    OUTER_TRACK_WIDTH = 1000
    OUTER_TRACK_HEIGHT = 700
    TRACK_THICKNESS = 220

    # Colors
    COLORS = {
        'WHITE': (255, 255, 255),
        'BLACK': (0, 0, 0),
        'GRAY': (128, 128, 128),
        'GREEN': (0, 255, 0)
    }

    # Create RaceTrack instance
    track = RaceTrack(WIDTH, HEIGHT, OUTER_TRACK_WIDTH, OUTER_TRACK_HEIGHT, TRACK_THICKNESS, COLORS)

    # Create Car instance
    car = AbstractCar(max_vel=4, rotation_vel=4)
    car.START_POS = (WIDTH // 2, HEIGHT // 2)  # Set starting position for the car

    # Main loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a]:
            car.rotate(left=True)
        if keys[pygame.K_d]:
            car.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            car.move_forward()
        if keys[pygame.K_s]:
            moved = True
            car.move_backward()

        if not moved:
            car.reduce_speed()

        if car.collide(track):
            #print("Collision detected!")
            # Handle collision (e.g., stop the car or reset position)
            car.bounce()
            
        # Draw everything
        track.draw()
        car.draw(track.window)

        pygame.display.flip()
        clock.tick(60)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
