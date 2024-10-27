import pygame
from car import AbstractCar, ComputerCar
from track import RaceTrack
import time
import math
import csv

# Colors
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128),
    'GREEN': (0, 255, 0)
}

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def draw_finish_line(screen, position, width, height, colors):
    x, y = position
    square_size = 10
    for row in range(height // square_size):
        for col in range(width // square_size):
            color = colors['BLACK'] if (row + col) % 2 == 0 else colors['WHITE']
            pygame.draw.rect(screen, color, (x + col * square_size, y + row * square_size, square_size, square_size))

def log_data(observation, action, log_file='driving_log.csv'):
    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        # Write the observation and action to the CSV file
        writer.writerow(observation + action)
start_time = time.time()

def main():
    pygame.init()

    # Game settings
    WIDTH, HEIGHT = 1250, 800
    OUTER_TRACK_WIDTH = 1000
    OUTER_TRACK_HEIGHT = 700
    TRACK_THICKNESS = 220

    # Log file setup
    log_file = 'driving_log.csv'
    # Initialize the CSV file with headers
    with open(log_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Position_X', 'Position_Y', 'Angle', 'Speed', 'Orientation','Velocity_Y',
            'Steering_Angle', 'Distance_1', 'Distance_2', 'Distance_3', 'Distance_4',
            'Distance_5', 'Distance_6', 'Distance_7', 'Distance_8', 'Total_Distance', 
            'Action_Steer', 'Action_Accelerate', 'Action_Brake'
        ])

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Race Track')
    
    # Create RaceTrack instance
    track = RaceTrack(WIDTH, HEIGHT, OUTER_TRACK_WIDTH, OUTER_TRACK_HEIGHT, TRACK_THICKNESS, COLORS)
    
    # Create Car instances
    car = AbstractCar(img_path="assets\\BlueStrip_1.png", max_vel=5, rotation_vel=4)
    computer = ComputerCar(img_path="assets\\GreenStrip.png", max_vel=5, rotation_vel=4)

    running = True
    clock = pygame.time.Clock()

    while running:
        total_distance = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        moved = False
        opponent_moved = False

        # Action defaults
        action_steer = 0
        action_accelerate = 0
        action_brake = 0

        # Player controls
        if keys[pygame.K_a]:
            car.rotate(left=True)
            action_steer = -1
        if keys[pygame.K_d]:
            car.rotate(right=True)
            action_steer = 1
        if keys[pygame.K_w]:
            moved = True
            car.move_forward()
            action_accelerate = 1
        if keys[pygame.K_s]:
            moved = True
            car.move_backward()
            action_brake = 1

        if not moved:
            car.reduce_speed()

        # Collisions
        if car.collide(track):
            car.bounce()
        if car.car_collide(computer):
            computer.bounce()
            car.bounce()

        # Check finish line
        if track.finish_line_collide(car):
            end_time = time.time()
            finishing_time = end_time - start_time
            print(f"Game Over! Finishing time: {finishing_time:.2f} seconds")
            

        # Get observations
        distances = car.get_distances_to_obstacles(track)
        position = car.get_position()
        orientation = car.get_orientation()
        velocity = car.get_velocity()
        steering_angle = car.get_steering_angle()

        # Compile observation and action
        observation = [
            position[0], position[1], car.get_angle(), car.get_speed(), orientation,
            velocity, steering_angle, *distances, total_distance
        ]
        action = [action_steer, action_accelerate, action_brake]

        # Log data
        log_data(observation, action, log_file)

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
