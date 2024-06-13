import pygame
import time
import math
from utils import scale, scale_car
from car import AbstractCar


GRASS = scale(pygame.image.load("assets\\grass.jpg"), 2.5)
TRACK = scale(pygame.image.load("assets\\track.png"), 0.9)

TRACK_BORDER = scale(pygame.image.load("assets\\track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.transform.scale(pygame.image.load("assets\\finish.png"), (125, 20))
FINISH_MASK = pygame.mask.from_surface(FINISH)

RED_CAR = pygame.image.load("assets\\red-car.png")
RED_CAR = pygame.transform.scale(RED_CAR, (30, 50))

GREEN_CAR = pygame.image.load("assets\\green-car.png")

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FINISH_POSITION = (255,190)

pygame.display.set_caption("Racing Game")

FPS = 60


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (330, 200)

def draw(win, images, player):
    for img, pos in images:
        win.blit(img, pos)
    
    player.draw(win)
    pygame.display.update()


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
player_car = PlayerCar(4, 4)



while run:
    clock.tick(FPS)

    draw(WIN, images, player_car)

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break


    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if finish_poi_collide != None:
        if finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            print("finished")
        
pygame.quit()




