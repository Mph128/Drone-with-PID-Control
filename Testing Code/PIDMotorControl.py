from re import A
import smbus			#import SMBus module of I2C
from time import sleep          #import
import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait because its too impatient

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio  # importing GPIO library

ESC = 18  # Connect the ESC in this GPIO pin

pi = pigpio.pi();

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC, 0)


max_value = 2000  # change this if your ESC's max value is different or leave it be
min_value = 700  # change this if your ESC's min value is different or leave it be
print ("For first time launch, select calibrate")
print ("Type the exact word for the function you want")
print ("calibrate OR manual OR control OR arm OR stop")

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")


def manual_drive():  # You will use this function to program your ESC if required
    print
    "You have selected manual option so give a value between 0 and you max value"
    while True:
        inp = input()
        if inp == "stop":
            stop()
            break
        elif inp == "control":
            control()
            break
        elif inp == "arm":
            arm()
            break

        else:
            piq.set_servo_pulsewidth(ESC, inp)

def calibrate():  # This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print(
            "Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(ESC, min_value)
            print("Wierd eh! Special tone")
            time.sleep(7)
            print ("Wait for it ....")
            time.sleep(5)
            print ("Im working on it, DONT WORRY JUST WAIT.....")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print ("Arming ESC now...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print ("See.... uhhhhh")
            controlMPU6050(1500,400,50,.1)  # You can change this to any other function you want


def control():
    print("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
    time.sleep(1)
    speed = 1500  # change your speed if you want to.... it should be between 700 - 2000
    print("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = input()

        if inp == "q":
            speed -= 100  # decrementing the speed like hell
            print
            "speed = %d" % speed
        elif inp == "e":
            speed += 100  # incrementing the speed like hell
            print
            "speed = %d" % speed
        elif inp == "d":
            speed += 10  # incrementing the speed
            print
            "speed = %d" % speed
        elif inp == "a":
            speed -= 10  # decrementing the speed
            print
            "speed = %d" % speed
        elif inp == "stop":
            stop()  # going for the stop function
            break
        elif inp == "manual":
            manual_drive()
            break
        elif inp == "arm":
            arm()
            break

        else:
            print ("WHAT DID I SAID!! Press a,q,d or e")



def averageMPU6050(sensitivity):
    Ax=0
    Gx=0
    for i in range(5):
            acc_x = read_raw_data(ACCEL_XOUT_H)
            gyro_x = read_raw_data(GYRO_YOUT_H)
            Ax+=acc_x
            Gx+=gyro_x
            time.sleep(sensitivity)
    Ax = Ax/81920.0
    Gx = Gx/655.0
    return (Ax,Gx)

def controlMPU6050(hoverSpeed,P,D,sensitivity):
    time.sleep(1)
    print("Motor Started")
    # change your speed if you want to.... it should be between 700 - 2000
    Ax=0
    Gx=0
    while True:
        Ax,Gx=averageMPU6050(sensitivity)
        speed = hoverSpeed + int(P*Ax) - int(D*Gx)
        print (Ax,"\n",Gx,"\n",speed,'  ',int(P*Ax),'  ',int(D*Gx))
        if speed>max_value:
            speed = max_value - 1

        elif speed < min_value:
            speed = min_value + 1

        pi.set_servo_pulsewidth(ESC, speed)



def arm():  # This is the arming procedure of an ESC
    print("Connect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        controlMPU6050(1500,1,1,1)


def stop():  # This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()


# This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.

inp = input()
if inp == "manual":
    manual_drive()
elif inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else:
    print("Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!")

