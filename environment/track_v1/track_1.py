# track.py
import pygame

class RaceTrack:
    def __init__(self, width, height, outer_track_width, outer_track_height, track_thickness, colors):
        self.width = width
        self.height = height
        self.outer_track_width = outer_track_width
        self.outer_track_height = outer_track_height
        self.track_thickness = track_thickness
        self.colors = colors
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Race Track')

        self.finish_line_img = self.create_finish_flag_image(215, 30, 10)
        self.finish_line_pos = (130, 300)

        self.calculate_positions()

    def calculate_positions(self):
        self.outer_track_rect = pygame.Rect(
            (self.width - self.outer_track_width ) // 2 ,
            (self.height - self.outer_track_height ) // 2,
            self.outer_track_width,
            self.outer_track_height
        )
        self.inner_track_rect = pygame.Rect(
            self.outer_track_rect.left + self.track_thickness,
            self.outer_track_rect.top + self.track_thickness,
            self.outer_track_width - 2 * self.track_thickness,
            self.outer_track_height - 2 * self.track_thickness
        )

    def create_finish_flag_image(self, width, height, square_size):
        """
        Create a finish flag image with a checkerboard pattern.

        :param width: The width of the finish flag image.
        :param height: The height of the finish flag image.
        :param square_size: The size of each square in the checkerboard pattern.
        :return: A Pygame Surface object with the finish flag image.
        """
        flag_img = pygame.Surface((width, height))
        black = (0, 0, 0)
        white = (255, 255, 255)

        num_cols = width // square_size
        num_rows = height // square_size
        for row in range(num_rows):
            for col in range(num_cols):
                color = black if (row + col) % 2 == 0 else white
                pygame.draw.rect(flag_img, color, (col * square_size, row * square_size, square_size, square_size))

        return flag_img
    

    def get_outer_track_rect(self):
        return self.outer_track_rect

    def get_inner_track_rect(self):
        return self.inner_track_rect

    def draw(self):
        self.window.fill(self.colors['WHITE'])

        # Draw the track
        pygame.draw.rect(self.window, self.colors['GRAY'], self.outer_track_rect)  # Outer track
        pygame.draw.rect(self.window, self.colors['GREEN'], self.inner_track_rect)  # Inner track

        # Draw track borders
        pygame.draw.rect(self.window, self.colors['BLACK'], self.outer_track_rect, 5)
        pygame.draw.rect(self.window, self.colors['BLACK'], self.inner_track_rect, 5)

        self.window.blit(self.finish_line_img, self.finish_line_pos)

        pygame.display.flip()

