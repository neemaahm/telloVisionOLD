import sys
import time

import cv2
from djitellopy import Tello
import pygame
from pygame.locals import *
# import test
# test.main()

#Initialize Pygame
pygame.init()
pygame.display.set_caption('Joystick ')
screen = pygame.display.set_mode((500, 250), 0, 32)
clock = pygame.time.Clock()

#Connect Controller
pygame.joystick.init()
gamepad = pygame.joystick.Joystick(0)

#Create Stick Rectangle Objects
leftStickRect = pygame.Rect(50, 50, 50, 50)
rightStickRect = pygame.Rect(50, 50, 50, 50)

#Create useful dictionary, lists, and variables
colors = {"red": (255, 0, 0), "green": (50, 125, 50), "blue": (0, 0, 255), "white": (255, 255, 255), "black": (0, 0, 0)}
buttonValues = [False] * 8
stickValues = [0, 0, 0, 0]
hatValues = [0,0]


while True:
    pygame.event.pump()

    #Take Pygame Input
    for i in range(len(stickValues)):
        stickValues[i] = gamepad.get_axis(i)
    for i in range(len(buttonValues)):
        buttonValues[i] = gamepad.get_button(i)
    hatValues = gamepad.get_hat(0)

    # Draw thumb-stick rectangles
    screen.fill(colors["green"])
    pygame.draw.rect(screen, colors["red"], leftStickRect)
    pygame.draw.rect(screen, colors["blue"], rightStickRect)
    if abs(stickValues[0]) < 0.1:
        stickValues[0] = 0
    if abs(stickValues[1]) < 0.1:
        stickValues[1] = 0
    leftStickRect.x = 100 + (stickValues[0] * 100)
    leftStickRect.y = 100 + (stickValues[1] * 100)
    rightStickRect.x = 350 + (stickValues[2] * 100)
    rightStickRect.y = 100 + (stickValues[3] * 100)

    pygame.display.update()
    clock.tick(60)