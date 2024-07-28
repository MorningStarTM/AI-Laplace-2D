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

    def draw(self, window):
        pygame.draw.rect(window, self.colors['GRAY'], self.outer_track_rect)  # Outer track
        pygame.draw.rect(window, self.colors['GREEN'], self.inner_track_rect)  # Inner track

        pygame.draw.rect(window, self.colors['BLACK'], self.outer_track_rect, 5)
        pygame.draw.rect(window, self.colors['BLACK'], self.inner_track_rect, 5)

        # Draw the finishing line
        self.draw_finish_line(window)

    def finish_line_collide(self, car):
        """
        Check if the car collides with the finish line.

        :param car: Instance of the car.
        :return: True if collision, otherwise False.
        """
        finish_line_rect = pygame.Rect(self.finish_line_position[0], self.finish_line_position[1], self.finish_line_width, self.finish_line_height)
        car_rect = car.get_rect()
        return finish_line_rect.colliderect(car_rect)
