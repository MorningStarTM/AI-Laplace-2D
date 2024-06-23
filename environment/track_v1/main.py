import pygame
from car import AbstractCar, ComputerCar
from track import RaceTrack

# Colors
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128),
    'GREEN': (0, 255, 0)
}

def main():
    pygame.init()

    # Game settings
    WIDTH, HEIGHT = 1250, 800
    OUTER_TRACK_WIDTH = 1000
    OUTER_TRACK_HEIGHT = 700
    TRACK_THICKNESS = 220

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Race Track')

    # Create RaceTrack instance
    track = RaceTrack(WIDTH, HEIGHT, OUTER_TRACK_WIDTH, OUTER_TRACK_HEIGHT, TRACK_THICKNESS, COLORS)

    # Create Car instances
    car = AbstractCar(img_path="assets/BlueStrip_1.png", max_vel=5, rotation_vel=4)
    computer = ComputerCar(img_path="assets/GreenStrip.png", max_vel=5, rotation_vel=4)

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        moved = False
        opponent_moved = False

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

        if keys[pygame.K_LEFT]:
            computer.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            computer.rotate(right=True)
        if keys[pygame.K_UP]:
            computer.move_forward()
            opponent_moved = True
        if keys[pygame.K_DOWN]:
            computer.move_backward()
            opponent_moved = True

        if not moved:
            car.reduce_speed()
        if not opponent_moved:
            computer.reduce_speed()

        if car.collide(track):
            car.bounce()
        if computer.collide(track):
            computer.bounce()

        if car.car_collide(computer):
            car.apply_collision_effect(computer)
            computer.apply_collision_effect(car)

        # Draw everything
        screen.fill(COLORS['WHITE'])  # Clear the screen with white color
        track.draw(screen)
        car.draw(screen)
        computer.draw(screen)

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
