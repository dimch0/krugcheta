import pygame, random
from pygame.locals import *
import time
from math import sqrt

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
grey = (195, 195, 195)
pink = (252, 217, 229)
green = (210, 255, 191)

FPS = 30
body_step = 1
fi = 30


display_width = 800
display_height = 600

mid_x = int((display_width-200)/2)
mid_y = int(display_height/2)


gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('radius')

clock = pygame.time.Clock()

def Tracks(point_A, Point_B, speed = 5):
    track = []
    ax = point_A[0]
    ay = point_A[1]
    bx = Point_B[0]
    by = Point_B[1]
    dx, dy = (bx - ax, by - ay)
    distance = sqrt(dx**2 + dy**2)

    steps_number = int(distance / speed)
    if steps_number > 0:
        stepx, stepy = int(dx / steps_number), int(dy / steps_number)
        for i in range(steps_number+1):
            step = [int(ax + stepx * i), int(ay + stepy * i)]
            track.append(step)
    # track.append(Point_B)
    return track


def game_loop():

    game_exit = False

    lead_x = 336
    lead_y = mid_y

    menu = False

    END_POINT = None
    COUNT = 0

    while not game_exit:

        # MOUSE POSITION X AND Y
        mouse_pos = pygame.mouse.get_pos()
        mx = mouse_pos[0]
        my = mouse_pos[1]

        for event in pygame.event.get():
            # print event
            if event.type == pygame.QUIT:

                game_exit = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("click", mouse_pos)
                track = Tracks((lead_x, lead_y), mouse_pos)
                print "trackes", track
                END_POINT = len(track)
                print "END_POINT", END_POINT
                COUNT = 0
                print "COUNT", COUNT


                if in_circle(lead_x, lead_y, fi, mx, my) and not menu:
                    menu = True
                    print menu
                else:
                    menu = False
                    print menu


        if END_POINT:
            #print "COUNTTTT", COUNT
            if not COUNT == END_POINT - 1:
                COUNT += 1
            lead_x = track[COUNT][0]
            lead_y = track[COUNT][1]

        # BACKGROUND
        gameDisplay.fill(black)


        # TODO blit stuff

        # GRID
        for x in range(0, 12):
            for y in range(1, 20):
                if x % 2 == y % 2:
                    pygame.draw.circle(gameDisplay, white, [fi + (x * 51), y * fi], fi, 1)

        if menu:
            pygame.draw.circle(gameDisplay, green, [lead_x, lead_y], fi * 3, 0)

        # body
        pygame.draw.circle(gameDisplay, pink, (lead_x, lead_y), fi, 0)
        # body range:
        pygame.draw.circle(gameDisplay, white, (lead_x, lead_y), 300, 1)


        pygame.display.update()


        # TODO: if change vars to blit
        clock.tick(FPS)

    pygame.quit()
    quit()


def in_circle(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2


game_loop()


asdasd

