
import cv2
from djitellopy import Tello
import pygame

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
colors = {"red": (255, 0, 0), "green": (50, 125, 50), "blue": (0, 0, 255)}
droneStates = {True:"Flying", False:"Landed"}
buttonValues = [False] * 8
stickValues = [0] * 4
hatValues = [0] * 2
flyState = False
doLoop = True

#Connect to Tello
tello = Tello()
tello.connect()
tello.streamon()
print("Tello Battery: " + str(tello.get_battery()))

#Shutdown sequence
def shutdown(droneStatus):
    print("Shutdown Started")
    try:
        if droneStatus:
            tello.land()
    finally:
        cv2.destroyAllWindows()
        pygame.quit()
        print("Shutdown Completed")
        return False

while doLoop == True:
    #Retrieve feed from Tello
    frame_read = tello.get_frame_read()
    liveFrame = frame_read.frame
    cv2.imshow("Tello Video Feed", liveFrame)

    # Take Pygame Input
    for i in range(len(stickValues)):
        stickValues[i] = gamepad.get_axis(i)
    for i in range(len(buttonValues)):
        buttonValues[i] = gamepad.get_button(i)
    hatValues = gamepad.get_hat(0)

    #Shutdown and land drone
    # if buttonValues[7]:
    #         doLoop = flyState = shutdown(flyState)

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

    #Move Tello
    horMultiplier = 60
    rotMultiplier = 90
    vertMultiplier = 20
    if flyState:
        #Left-Right Translation
        if stickValues[0] > 0.4:
            tello.move_right(int(stickValues[0] * horMultiplier))
        elif stickValues[0] < -0.4:
            tello.move_left(abs(int(stickValues[0] * horMultiplier)))
        #Forward-Back Translation
        if stickValues[1] > 0.4:
            tello.move_back(int(stickValues[1] * horMultiplier))
        elif stickValues[1] < -0.4:
            tello.move_forward(abs(int(stickValues[1] * horMultiplier)))
        #Yaw Rotation
        if stickValues[2] > 0.1:
            tello.rotate_clockwise(int(stickValues[2]*rotMultiplier))
        elif stickValues[2] < -0.1:
            tello.rotate_counter_clockwise(abs(int(stickValues[2]*rotMultiplier)))
        #Vertical Translation
        if hatValues[1] > 0:
            tello.move_up(vertMultiplier)
        elif hatValues[1] < 0:
            tello.move_down(vertMultiplier)

    pygame.display.update()
    clock.tick(60)

print("END")
