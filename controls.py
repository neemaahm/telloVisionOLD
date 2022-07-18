#Neema Ahmadian - Collab - July 2022

import cv2
import pygame

#This class takes care of all things GUI related for the Tello Drone project
class controls:
    def __init__(self):
        # Connect Controller
        pygame.joystick.init()
        self.gamepad = pygame.joystick.Joystick(0)

        #Create Drone and Controller State Variables
        self.drone_states = {True: "Flying", False: "Landed"}
        self.button_values = [False] * 8
        self.stick_values = [0] * 4
        self.hat_values = [0] * 2
        self.fly_state = False
        self.do_loop = True

    #Connect Individual Tello Drone
    def connect_drone(self, tello_drone):
        # Connect to Tello
        tello_drone.connect()
        tello_drone.streamon()
        print("Tello Battery: " + str(tello_drone.get_battery()))

    #Connects Tello Swarm
    # def connect_swarm(self, tello_swarm):
    #     swarm.connect()

    #Shutdown Sequence
    def drone_shutdown(self, fly_status, tello_drone):
        print("Shutdown Started")
        try:
            if fly_status:
                tello_drone.land()
        finally:
            self.do_loop = False
            self.fly_state = False
            cv2.destroyAllWindows()
            pygame.quit()
            print("Shutdown Completed")
            return False

    #Checks for Shutdown and does Shutdown
    def check_shutdown(self, tello_drone):
        if self.button_values[7]:
            self.drone_shutdown(self.fly_state, tello_drone)

    #Takes All Inputs and Updates Corresponding Variables
    def take_inputs(self):
        # Take Pygame Inputs
        for i in range(len(self.stick_values)):
            self.stick_values[i] = self.gamepad.get_axis(i)
        for i in range(len(self.button_values)):
            self.button_values[i] = self.gamepad.get_button(i)
        self.hat_values = self.gamepad.get_hat(0)

        # Round Down Small Stick Values
        if abs(self.stick_values[0]) < 0.1:
            self.stick_values[0] = 0
        if abs(self.stick_values[1]) < 0.1:
            self.stick_values[1] = 0

    #Move Tello
    def move_tello(self, tello_drone, hor_mult, rot_mult, vert_mult):
        if self.stick_values[0] > 0.4:
            tello_drone.move_right(int(self.stick_values[0] * hor_mult))
        elif self.stick_values[0] < -0.4:
            tello_drone.move_left(abs(int(self.stick_values[0] * hor_mult)))
        #Forward-Back Translation
        if self.stick_values[1] > 0.4:
            tello_drone.move_back(int(self.stick_values[1] * hor_mult))
        elif self.stick_values[1] < -0.4:
            tello_drone.move_forward(abs(int(self.stick_values[1] * hor_mult)))
        #Yaw Rotation
        if self.stick_values[2] > 0.1:
            tello_drone.rotate_clockwise(int(self.stick_values[2] * rot_mult))
        elif self.stick_values[2] < -0.1:
            tello_drone.rotate_counter_clockwise(abs(int(self.stick_values[2] * rot_mult)))
        #Vertical Translation
        if self.hat_values[1] > 0:
            tello_drone.move_up(vert_mult)
        elif self.hat_values[1] < 0:
            tello_drone.move_down(vert_mult)
        # Square Translation
        if not self.hat_values[0] == 0:
            tello_drone.move_right(100)
            tello_drone.move_forward(100)
            tello_drone.move_left(100)
            tello_drone.move_back(100)
