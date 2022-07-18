import cv2
from djitellopy import Tello

def main():
    #Connect to Tello
    tello = Tello()
    tello.connect()
    print("Tello Battery: " + str(tello.get_battery()))
    tello.streamon()

    # Running loop
    while True:

        # Retrieve image from Tello
        frame_read = tello.get_frame_read()
        liveFrame = frame_read.frame
        cv2.imshow("Tello Video Feed", liveFrame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()