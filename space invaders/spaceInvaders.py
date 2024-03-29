import pygame
import sys
from AliveEntity import AliveEntity
from Player import Player
from Game import Game

pygame.init()

size = width, height = 448, 512
white = 255, 255, 255

def spawnNewAlien(i, j):
    startPosx = width/2 -1400 + 30 * i
    startPosy = height/2 - 130 + 30 * j
    imageName = "img/sprite" + str(j+1) + ".png"
    newAlien = AliveEntity(5 * (6 - j), startPosx, startPosy, 4, 0, imageName, 1, width, height)
    newAlien.posBoundaryLeft = 50 + 30 * i
    newAlien.posBoundaryRight= width -50 - 30 * (10 - i)
    return newAlien

def createAliens(cols, rows):
    aliens = []
    for i in range(cols):
        row = []
        for j in range(rows):
            newAlien = spawnNewAlien(i, j)
            row.append(newAlien)
        aliens.append(row)
    return aliens

def printEndMessage(message):
    text = game.display.font.render(message, 1, white)
    textRect = text.get_rect()
    textRect.x = width/2
    textRect.y = height/2
    game.screen.blit(text, textRect)
    pygame.display.flip()

def runGame(game, clock):
    while game.isRunning():
        game.update()
        pygame.display.flip()
        clock.tick(300)

clock = pygame.time.Clock()
aliens = createAliens(11, 5)
player = Player(-100, 3, width, height)
game = Game(0, aliens, player, width, height, size)

runGame(game, clock)

print("END")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            break
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_SPACE]:
        break
    if not game.aliensExist:
        printEndMessage("YOU WON!")
    else:
        printEndMessage("YOU LOST.")
    clock.tick(300)
pygame.quit()
