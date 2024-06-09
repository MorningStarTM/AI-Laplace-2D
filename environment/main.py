import pygame
import time
import math
from utils import scale
from car import AbstractCar


GRASS = scale(pygame.image.load("assets\\grass.jpg"), 2.5)
TRACK = scale(pygame.image.load("assets\\track.png"), 0.9)

TRACK_BORDER = scale(pygame.image.load("assets\\track-border.png"), 0.9)
FINISH = pygame.image.load("assets\\finish.png")

RED_CAR = pygame.image.load("assets\\red-car.png")
GREEN_CAR = pygame.image.load("assets\\green-car.png")

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

FPS = 60


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)

def draw(win, images, player):
    for img, pos in images:
        win.blit(img, pos)
    
    player.draw(win)
    pygame.display.update()


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0))]
player_car = PlayerCar(4, 4)



while run:
    clock.tick(FPS)

    draw(WIN, images, player_car)

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        
pygame.quit()




