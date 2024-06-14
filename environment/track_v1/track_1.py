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

    def draw(self):
        self.window.fill(self.colors['WHITE'])

        # Draw the track
        pygame.draw.rect(self.window, self.colors['GRAY'], self.outer_track_rect)  # Outer track
        pygame.draw.rect(self.window, self.colors['GREEN'], self.inner_track_rect)  # Inner track

        # Draw track borders
        pygame.draw.rect(self.window, self.colors['BLACK'], self.outer_track_rect, 5)
        pygame.draw.rect(self.window, self.colors['BLACK'], self.inner_track_rect, 5)

        pygame.display.flip()

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

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the track
        track.draw()

    # Quit Pygame
    pygame.quit()

