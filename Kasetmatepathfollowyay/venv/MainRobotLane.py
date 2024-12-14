from MotorModule import Motor
from LaneDetectionModule import getLaneCurve
import WebcamModule 
import cv2
#from buildhat import ColorDistanceSensor

motor = Motor(2,3,4,17,22,27)

def main() :

    img = WebcamModule.getImg()
    curveVal= getLaneCurve(img,1)

    sen = 1.3 #sensitivity
    maxVal = 0.3 #max speed 
    if curveVal>0 :
        sen=1.7
        if curveVal<0.05: curveVal=0
    else:
        if curveVal>-0.08: curveVal=0
    motor.move(0.20,-curveVal*sen,0.05) #might not need the minus
    cv2.waitKey(1)

if __name__ == '__main__':
    while True :
        main()

### adding in object detection from colordistance sensor from buildHAT 
""" from MotorModule import Motor
from LaneDetectionModule import getLaneCurve
import WebcamModule
from buildhat import ColorDistanceSensor
import cv2

# Initialize Motor, Sensor, and Joystick Mode (Placeholder for actual joystick code)
motor = Motor(2, 3, 4, 17, 22, 27)
color_distance_sensor = ColorDistanceSensor('A')  # Adjust port as needed

def activateJoystickMode():
    # Code to enable joystick control (depends on your joystick setup)
    print("Switched to Joystick Mode")

def main():
    img = WebcamModule.getImg()
    curveVal = getLaneCurve(img, 1)

    # Get color and distance from sensor
    color, distance = color_distance_sensor.get_color(), color_distance_sensor.get_distance()
    print(f"Color: {color}, Distance: {distance} cm")  # For debugging purposes

    # Stop motor and switch to joystick if a large, specific color object is detected
    if color != 'white' and distance is not None and distance < 30:  # Detect non-path color (assuming path is white)
        motor.move(0, 0, 0)  # Stop the motor
        activateJoystickMode()  # Switch to joystick control
        cv2.putText(img, "Object Detected - Switched to Joystick Mode", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        # Normal lane following behavior
        sen = 1.3  # sensitivity
        maxVal = 0.3  # max speed
        if curveVal > 0:
            sen = 1.7
            if curveVal < 0.05:
                curveVal = 0
        else:
            if curveVal > -0.08:
                curveVal = 0
        motor.move(0.20, -curveVal * sen, 0.05)  # Adjust as needed
    
    # Display output
    cv2.imshow("Output", img)
    cv2.waitKey(1)

if __name__ == '__main__':
    while True:
        main()
"""
