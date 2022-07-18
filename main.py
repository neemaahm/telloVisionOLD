from djitellopy import Tello
import pygame
import controls
import myGUI

myGUI = myGUI.myGUI()
controls = controls.controls()

tello = Tello()
controls.connect_drone(tello)

while controls.do_loop:
    myGUI.doVideoFeed(tello)
    controls.take_inputs()
    controls.check_shutdown(tello)
    myGUI.drawRectangles(controls.stick_values)
    controls.move_tello(tello, 60, 90, 20)

    pygame.display.update()
    myGUI.clock.tick(60)