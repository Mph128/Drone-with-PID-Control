from re import A
import smbus			#import SMBus module of I2C
from time import sleep          #import
import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait because its too impatient

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio  # importing GPIO library

ESC1 = 5  # Connect the ESC in this GPIO pin
ESC2 = 6
ESC3 = 13
ESC4 = 19

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC1, 0)
pi.set_servo_pulsewidth(ESC2, 0)
pi.set_servo_pulsewidth(ESC3, 0)
pi.set_servo_pulsewidth(ESC4, 0)

max_value = 2000  #ESC's max value
min_value = 700  #ESC's min value


def calibrate():  # This is the calibration procedure of an ESC
    pi.set_servo_pulsewidth(ESC1, 0)
    pi.set_servo_pulsewidth(ESC2, 0)
    pi.set_servo_pulsewidth(ESC3, 0)
    pi.set_servo_pulsewidth(ESC4, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC1, max_value)
        pi.set_servo_pulsewidth(ESC2, max_value)
        pi.set_servo_pulsewidth(ESC3, max_value)
        pi.set_servo_pulsewidth(ESC4, max_value)
        print(
            "Connect the battery now, wait for tones, then press Enter")
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(ESC1, min_value)
            pi.set_servo_pulsewidth(ESC2, min_value)
            pi.set_servo_pulsewidth(ESC3, min_value)
            pi.set_servo_pulsewidth(ESC4, min_value)
            print("Tones play")
            time.sleep(7)
            time.sleep(5)
            pi.set_servo_pulsewidth(ESC1, 0)
            pi.set_servo_pulsewidth(ESC2, 0)
            pi.set_servo_pulsewidth(ESC3, 0)
            pi.set_servo_pulsewidth(ESC4, 0)
            time.sleep(2)
            print ("Arming ESC")
            pi.set_servo_pulsewidth(ESC1, min_value)
            pi.set_servo_pulsewidth(ESC2, min_value)
            pi.set_servo_pulsewidth(ESC3, min_value)
            pi.set_servo_pulsewidth(ESC4, min_value)
            time.sleep(1)
            print ("Armed")
            control()  # You can change this to any other function you want



def control():
    print("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
    time.sleep(1)
    speed = 1300  # change your speed if you want to.... it should be between 700 - 2000
    print("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:
        pi.set_servo_pulsewidth(ESC1, speed)
        pi.set_servo_pulsewidth(ESC2, speed)
        pi.set_servo_pulsewidth(ESC3, speed)
        pi.set_servo_pulsewidth(ESC4, speed)
        inp = input()

        if inp == "q":
            speed -= 100  # decrementing the speed like hell
            print("speed = %d") % speed
        elif inp == "e":
            speed += 100  # incrementing the speed like hell
            print("speed = %d") % speed
        elif inp == "d":
            speed += 10  # incrementing the speed
            print("speed = %d") % speed
        elif inp == "a":
            speed -= 10  # decrementing the speed
            print("speed = %d") % speed
        elif inp == "stop":
            stop()  # going for the stop function
            break
        elif inp == "arm":
            arm()
            break

        else:
            print ("WHAT DID I SAID!! Press a,q,d or e")



def arm():  # This is the arming procedure of an ESC
    print("Connect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC1, 0)
        pi.set_servo_pulsewidth(ESC2, 0)
        pi.set_servo_pulsewidth(ESC3, 0)
        pi.set_servo_pulsewidth(ESC4, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC1, max_value)
        pi.set_servo_pulsewidth(ESC2, max_value)
        pi.set_servo_pulsewidth(ESC3, max_value)
        pi.set_servo_pulsewidth(ESC4, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC1, min_value)
        pi.set_servo_pulsewidth(ESC2, min_value)
        pi.set_servo_pulsewidth(ESC3, min_value)
        pi.set_servo_pulsewidth(ESC4, min_value)
        time.sleep(1)
        control()


def stop():  # This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC1, 0)
    pi.set_servo_pulsewidth(ESC2, 0)
    pi.set_servo_pulsewidth(ESC3, 0)
    pi.set_servo_pulsewidth(ESC4, 0)
    pi.stop()



hover=1500
proportional=300
derivative=50
cycleTime=.02

print ("For first time launch, select calibrate")
print ("Type the exact word for the function you want")
print ("calibrate OR control OR arm OR stop")

inp = input()

if inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else:
    print("Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!")

