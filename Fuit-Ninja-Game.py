import pygame, sys
import os
import random
#testing
#initializing useful variables
player_lives = 3
score = 0
fruits = ["melon", "orange", "pomegranate", "guava", "bomb"]
WIDTH = 900
HEIGHT = 500
FPS = 60


pygame.init()
pygame.display.set_caption("SLICE STORM")
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


background = pygame.image.load("Wood_backgroud.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
font = pygame.font.Font(os.path.join(os.getcwd(), ("Ninja_font.otf")), 32)#Have to put font
Fruits_logo = pygame.image.load("Fruit_logo.png")
Fruits_logo = pygame.transform.scale(Fruits_logo, (75, 75))
score_text = font.render( str(score), True, (BLACK))
score_text = pygame.transform.scale(score_text, (40, 40))

Heart_Icon = pygame.image.load("Lives_icon.png")
Heart_Icon = pygame.transform.scale(Heart_Icon, (70, 70))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game logic here

    # Clear the screen
    gameDisplay.fill((0, 0, 0))

    # Draw objects and text
    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (77, 20))
    gameDisplay.blit(Fruits_logo, (5, 0))
    Live_1 = gameDisplay.blit(Heart_Icon, (730,0))
    Live_2 = gameDisplay.blit(Heart_Icon, (780,0))
    Live_3 = gameDisplay.blit(Heart_Icon, (830,0))

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
