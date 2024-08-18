import pygame
from car import AbstractCar, ComputerCar
from track import RaceTrack
import time

# Colors
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128),
    'GREEN': (0, 255, 0)
}

def draw_finish_line(screen, position, width, height, colors):
    """
    Draw a finishing line with black and white checkered pattern.

    :param screen: Pygame surface to draw on.
    :param position: Tuple (x, y) representing the top-left position of the finish line.
    :param width: Width of the finishing line.
    :param height: Height of the finishing line.
    :param colors: Dictionary with 'BLACK' and 'WHITE' colors.
    """
    x, y = position
    square_size = 10  # Size of each square in the checkered pattern

    for row in range(height // square_size):
        for col in range(width // square_size):
            color = colors['BLACK'] if (row + col) % 2 == 0 else colors['WHITE']
            pygame.draw.rect(screen, color, (x + col * square_size, y + row * square_size, square_size, square_size))

colors = {'BLACK': (0, 0, 0), 'WHITE': (255, 255, 255)}
finish_line_position = (400, 50)  # Example position
finish_line_width = 100  # Example width
finish_line_height = 20  # Example height

clock = pygame.time.Clock()

start_time = time.time()

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
    
    points_lap = []

    # Create RaceTrack instance
    track = RaceTrack(WIDTH, HEIGHT, OUTER_TRACK_WIDTH, OUTER_TRACK_HEIGHT, TRACK_THICKNESS, COLORS)
    
    # Create Car instances
    car = AbstractCar(img_path="assets\\BlueStrip_1.png", max_vel=5, rotation_vel=4)
    computer = ComputerCar(img_path="assets\\GreenStrip.png", max_vel=5, rotation_vel=4)

    running = True
    clock = pygame.time.Clock()
    timeframe = 0

    car_on_point_line = False  # Track whether the car is on the point line

    while running:
        timeframe += 1
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
            computer.bounce()
            car.bounce()

        if track.start_line_collide(car):
            car.bounce()
        if track.finish_line_collide(car):
            end_time = time.time()
            finishing_time = end_time - start_time
            print(f"Game Over! Finishing time: {finishing_time:.2f} seconds -- Frame {timeframe}")
            running = False

        if track.point_A_line_collide(car):
            if not car_on_point_line:
                print(f"Point line crossed! -- Frame {points_lap}")
                if 'A' not in points_lap:
                    points_lap.append('A')
                car_on_point_line = True
        else:
            car_on_point_line = False

        if track.point_B_line_collide(car):
            if not car_on_point_line:
                print(f"Point line crossed! -- Frame {points_lap}")
                if 'B' not in points_lap:
                    points_lap.append('B')
                car_on_point_line = True
        else:
            car_on_point_line = False

        if track.point_C_line_collide(car):
            if not car_on_point_line:
                print(f"Point line crossed! -- Frame {points_lap}")
                if 'C' not in points_lap:
                    points_lap.append('C')
                car_on_point_line = True
        else:
            car_on_point_line = False

        # Get observations
        distances = car.get_distances_to_obstacles(track)
        position = car.get_position()
        orientation = car.get_orientation()
        velocity = car.get_velocity()
        steering_angle = car.get_steering_angle()

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