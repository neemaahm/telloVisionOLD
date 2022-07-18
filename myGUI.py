#Neema Ahmadian - Collab - July 2022
import cv2
import pygame

#This class takes care of all things GUI related for the Tello Drone project
class myGUI:
    def __init__(self):
        #Initialize Pygame
        pygame.init()
        pygame.display.set_caption('Gamepad Inputs')
        self.screen = pygame.display.set_mode((500, 250), 0, 32)
        self.clock = pygame.time.Clock()

        # Create Stick Rectangle Objects
        self.left_stick_rect = pygame.Rect(50, 50, 50, 50)
        self.right_stick_rect = pygame.Rect(50, 50, 50, 50)
        self.colors = {"red": (255, 0, 0),
                       "green": (50, 125, 50),
                       "blue": (0, 0, 255)}

    #Retrieve & Display Tello Video Feed
    def doVideoFeed(self, telloDrone):
        self.frame_read = telloDrone.get_frame_read()
        self.live_frame = self.frame_read.frame
        cv2.imshow("Tello Video Feed", self.live_frame)

    # Draw Thumb-Stick GUI Rectangles
    def drawRectangles(self, stick_values):
        self.screen.fill(self.colors["green"])
        pygame.draw.rect(self.screen, self.colors["red"], self.left_stick_rect)
        pygame.draw.rect(self.screen, self.colors["blue"], self.right_stick_rect)
        self.left_stick_rect.x = 100 + (stick_values[0] * 100)
        self.left_stick_rect.y = 100 + (stick_values[1] * 100)
        self.right_stick_rect.x = 350 + (stick_values[2] * 100)
        self.right_stick_rect.y = 100 + (stick_values[3] * 100)
