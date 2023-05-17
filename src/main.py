# -*- coding: utf-8 -*-
import os
import pygame
from engine.Marias import Marias
from config import *


dir_path = os.path.dirname(os.path.realpath(__file__))


WIDTH, HEIGHT = 1200, 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Matrimony_card_game")

pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


FPS = 10

LEVEL_FONT = pygame.font.SysFont("comicsans", 20)

TURN = pygame.image.load(dir_path + "/engine/assets/turn.png")


CARD_WIDTH = 60
CARD_HEIGHT = 80


def draw_window(marias: Marias):
    #WIN.blit(SEA, (0, 0))
    WIN.fill(WHITE)

    h1 = LEVEL_FONT.render("Hrac 0: " + marias.player0.name +
                           " ::: Skore: " + str(marias.player0points), 1, BLACK)
    h2 = LEVEL_FONT.render("Hrac 1: " + marias.player1.name +
                           " ::: Skore: " + str(marias.player1points), 1, BLACK)
    h3 = LEVEL_FONT.render("Trumfy: ", 1, BLACK)

    WIN.blit(h1, (30, 30))
    WIN.blit(h2, (30, 660))
    WIN.blit(h3, (1000, 10))

    #WIN.blit(FLAG, (WIDTH - ME_SIZE, HEIGHT - ME_SIZE - 10))

    # for mine in mines:
    #    WIN.blit(ENEMY, (mine.rect.x, mine.rect.y))

    # cards of player 1 (top)
    x = 50
    y = 70
    for c in marias.player0.hand.cards:
        WIN.blit(c.picture, (x, y))
        x += 70

    # cards of player 2 (down)
    x = 50
    y = 550
    for c in marias.player1.hand.cards:
        WIN.blit(c.picture, (x, y))
        x += 70

    # draw history
    x = 50
    y = 250
    for stych in marias.history.stychy:
        c0 = stych.card0
        c1 = stych.card1

        if c0 != None:
            d = 0
            if stych.hlaska0:
                d = 20
            WIN.blit(c0.picture, (x, y-d))

        if c1 != None:
            d = 0
            if stych.hlaska1:
                d = 20
            WIN.blit(c1.picture, (x, y+120+d))

        wt = stych.wt

        if wt == 0:
            WIN.blit(TURN, (x+20, y-50))
        if wt == 1:
            WIN.blit(TURN, (x+20, y+250))

        x += 70

    WIN.blit(marias.lastcard.picture, (1000, 50))
    pygame.draw.line(WIN, BLACK, (814, 200), (814, 520), 3)

    pygame.display.update()


# hlavni smycka hry
def main():

    marias = Marias()

    clock = pygame.time.Clock()

    run = True

    while run:

        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()

        # herni kolo - stridaji se tahy hracu
        if keys_pressed[pygame.K_SPACE] and not marias.isdone():
            # if not marias.isdone():
            marias.play()

        draw_window(marias)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == "__main__":
    main()
