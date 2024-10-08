import pygame

class RaceTrack:
    def __init__(self, width, height, outer_track_width, outer_track_height, track_thickness, colors):
        self.width = width
        self.height = height
        self.outer_track_width = outer_track_width
        self.outer_track_height = outer_track_height
        self.track_thickness = track_thickness
        self.colors = colors

        # Finish line properties
        self.finish_line_width = 220
        self.finish_line_height = 30
        self.finish_line_position = (100, 380)

        # Start line properties (behind the car)
        self.start_line_height = 10  # Height of the start line
        self.start_line_position = (100, self.finish_line_position[1] + self.finish_line_height + 10)
        self.point = [(600, 50), (905, 400), (600, 530)]

        self.calculate_positions()

    def calculate_positions(self):
        self.outer_track_rect = pygame.Rect(
            (self.width - self.outer_track_width) // 2,
            (self.height - self.outer_track_height) // 2,
            self.outer_track_width,
            self.outer_track_height
        )
        self.inner_track_rect = pygame.Rect(
            self.outer_track_rect.left + self.track_thickness,
            self.outer_track_rect.top + self.track_thickness,
            self.outer_track_width - 2 * self.track_thickness,
            self.outer_track_height - 2 * self.track_thickness
        )
        
        self.finish_line_position = (125, 380)
        self.start_line_position = (self.finish_line_position[0], 370)

    def get_outer_track_rect(self):
        return self.outer_track_rect

    def get_inner_track_rect(self):
        return self.inner_track_rect

    def draw_finish_line(self, window):
        """
        Draw a finishing line with black and white checkered pattern.

        :param window: Pygame surface to draw on.
        """
        x, y = self.finish_line_position
        square_size = 10  # Size of each square in the checkered pattern

        for row in range(self.finish_line_height // square_size):
            for col in range(self.finish_line_width // square_size):
                color = self.colors['BLACK'] if (row + col) % 2 == 0 else self.colors['WHITE']
                pygame.draw.rect(window, color, (x + col * square_size, y + row * square_size, square_size, square_size))

    def draw_start_line(self, window):
        """
        Draw the start line (black line) just behind the car and in front of the finish line.

        :param window: Pygame surface to draw on.
        """
        x, y = self.start_line_position
        pygame.draw.rect(window, self.colors['BLACK'], (x, y, self.finish_line_width, self.start_line_height))


    def point_A_line(self, window, pos:tuple, size:tuple):
        """
        Draw the start line (black line) just behind the car and in front of the finish line.

        :param window: Pygame surface to draw on.
        """
        x, y = pos
        width, height = size
        pygame.draw.rect(window, self.colors['BLACK'], (x, y, width, height))

    def point_B_line(self, window, pos:tuple, size:tuple):
        """
        Draw the start line (black line) just behind the car and in front of the finish line.

        :param window: Pygame surface to draw on.
        """
        x, y = pos
        width, height = size
        pygame.draw.rect(window, self.colors['BLACK'], (x, y, width, height))
    
    def point_C_line(self, window, pos:tuple, size:tuple):
        """
        Draw the start line (black line) just behind the car and in front of the finish line.

        :param window: Pygame surface to draw on.
        """
        x, y = pos
        width, height = size
        pygame.draw.rect(window, self.colors['BLACK'], (x, y, width, height))


    def point_line(self, window, pos:tuple, size:tuple):
        """
        Draw the start line (black line) just behind the car and in front of the finish line.

        :param window: Pygame surface to draw on.
        """
        x, y = pos
        width, height = size
        pygame.draw.rect(window, self.colors['GRAY'], (x, y, width, height))


    def draw(self, window):
        pygame.draw.rect(window, self.colors['GRAY'], self.outer_track_rect)  # Outer track
        pygame.draw.rect(window, self.colors['GREEN'], self.inner_track_rect)  # Inner track

        pygame.draw.rect(window, self.colors['BLACK'], self.outer_track_rect, 5)
        pygame.draw.rect(window, self.colors['BLACK'], self.inner_track_rect, 5)

        # Draw the finishing line
        self.draw_finish_line(window)

        # Draw the start line (anti-cheat line)
        self.draw_start_line(window)
        self.point_A_line(window, self.point[0], (2, 220))
        self.point_B_line(window, self.point[1], (220, 2))
        self.point_C_line(window, self.point[2], (2, 220))

        self.point_line(window, (128, 200), (220, 2))   #
        self.point_line(window, (960, 50), (2, 220))
        self.point_line(window, (900, 590), (220, 2))
        self.point_line(window, (300, 530), (2, 220))

    def finish_line_collide(self, car):
        """
        Check if the car collides with the finish line.

        :param car: Instance of the car.
        :return: True if collision, otherwise False.
        """
        finish_line_rect = pygame.Rect(self.finish_line_position[0], self.finish_line_position[1], self.finish_line_width, self.finish_line_height)
        car_rect = car.get_rect()
        return finish_line_rect.colliderect(car_rect)

    def start_line_collide(self, car):
        """
        Check if the car collides with the start line (anti-cheat line).

        :param car: Instance of the car.
        :return: True if collision, otherwise False.
        """
        start_line_rect = pygame.Rect(self.start_line_position[0], self.start_line_position[1], self.finish_line_width, self.start_line_height)
        car_rect = car.get_rect()
        return start_line_rect.colliderect(car_rect)
    
    def point_line_collide(self, pos:tuple, size:tuple, car):
        """
        Check if the car collides with the point line.

        :param car: Instance of the car.
        :return: True if collision, otherwise False.
        """
        point_line_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        car_rect = car.get_rect()
        return point_line_rect.colliderect(car_rect)
    

    def point_A_line_collide(self, car):
        """
        Check if the car collides with the point line.

        :param car: Instance of the car.
        :return: True if collision, otherwise False.
        """
        point_line_rect = pygame.Rect(self.point[0][0], self.point[0][1], 2, 220)
        car_rect = car.get_rect()
        return point_line_rect.colliderect(car_rect)
    
    def point_B_line_collide(self, car):
        """
        Check if the car collides with the point line.

        :param car: Instance of the car.
        :return: True if collision, otherwise False.
        """
        point_line_rect = pygame.Rect(self.point[1][0], self.point[1][1], 220, 2)
        car_rect = car.get_rect()
        return point_line_rect.colliderect(car_rect)
    

    def point_C_line_collide(self, car):
        """
        Check if the car collides with the point line.

        :param car: Instance of the car.
        :return: True if collision, otherwise False.
        """
        point_line_rect = pygame.Rect(self.point[2][0], self.point[2][1], 2, 220)
        car_rect = car.get_rect()
        return point_line_rect.colliderect(car_rect)