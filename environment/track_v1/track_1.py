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

        pygame.display.flip()

