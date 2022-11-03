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

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC1, 0)
pi.set_servo_pulsewidth(ESC2, 0)
pi.set_servo_pulsewidth(ESC3, 0)
pi.set_servo_pulsewidth(ESC4, 0)

max_value = 2000  #ESC's max value
min_value = 700  #ESC's min value

def calibrate(h,p,d,s):  # This is the calibration procedure of an ESC
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
            controlMPU6050(h,p,d,s)  # You can change this to any other function you want



def averageMPU6050(sensitivity):
    Ax=0
    Gx=0
    Ay=0
    Gy=0
    az=0
    gz=0
    for i in range(5):
            Ax,Ay,az,Gx,Gy,gz = mpu6050_conv()
            time.sleep(sensitivity)
    Ax = Ax/5
    Gx = Gx/5
    Ay = Ay/5
    Gy = Gy/5
    return (Ax,Gx,Ay,Gy)


def controlMPU6050(hoverSpeed,P,D,sensitivity):
    time.sleep(1)
    print("Motor Started")
    Ax=0
    Gx=0
    startSpeed=1300
    pi.set_servo_pulsewidth(ESC1, startSpeed)
    pi.set_servo_pulsewidth(ESC2, startSpeed)
    pi.set_servo_pulsewidth(ESC3, startSpeed)
    pi.set_servo_pulsewidth(ESC4, startSpeed)
    time.sleep(5)
    while (startSpeed<(hoverSpeed-100)):
        pi.set_servo_pulsewidth(ESC1, startSpeed)
        pi.set_servo_pulsewidth(ESC2, startSpeed)
        pi.set_servo_pulsewidth(ESC3, startSpeed)
        pi.set_servo_pulsewidth(ESC4, startSpeed)
        startSpeed += 25
        time.sleep(.1)
    
    while True:

        Ax,Gx,Ay,Gy=averageMPU6050(sensitivity)

        speed1 = hoverSpeed + int(P*Ax) - int(D*Gx) - int(P*Ay) + int(D*Gy)
        speed2 = hoverSpeed - int(P*Ax) + int(D*Gx) + int(P*Ay) - int(D*Gy)
        speed3 = hoverSpeed - int(P*Ax) + int(D*Gx) - int(P*Ay) + int(D*Gy)
        speed4 = hoverSpeed + int(P*Ax) - int(D*Gx) + int(P*Ay) - int(D*Gy)

        if speed1>max_value:
            speed1 = max_value - 1
        elif speed1 < 900:
            speed1 = 900

        if speed2>max_value:
            speed2 = max_value - 1
        elif speed2 < 900:
            speed2 = 900

        if speed3>max_value:
            speed3 = max_value - 1
        elif speed3 < 900:
            speed3 = 900

        if speed4>max_value:
            speed4 = max_value - 1
        elif speed4 < 900:
            speed4 = 900

        pi.set_servo_pulsewidth(ESC1, speed1)
        pi.set_servo_pulsewidth(ESC2, speed2)
        pi.set_servo_pulsewidth(ESC3, speed3)
        pi.set_servo_pulsewidth(ESC4, speed4)



def arm(h,p,d,s):  # This is the arming procedure of an ESC
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
        controlMPU6050(h,p,d,s)


def stop():  # This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC1, 0)
    pi.set_servo_pulsewidth(ESC2, 0)
    pi.set_servo_pulsewidth(ESC3, 0)
    pi.set_servo_pulsewidth(ESC4, 0)
    pi.stop()



hover=1400
proportional=150
derivative=50
cycleTime=.01

print ("For first time launch, select calibrate")
print ("Type the exact word for the function you want")
print ("calibrate OR manual OR control OR arm OR stop")

inp = input()

if inp == "calibrate":
    calibrate(hover,proportional,derivative,cycleTime)
elif inp == "arm":
    arm(hover,proportional,derivative,cycleTime)
elif inp == "control":
    controlMPU6050(hover,proportional,derivative,cycleTime)
elif inp == "stop":
    stop()
else:
    print("Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!")

