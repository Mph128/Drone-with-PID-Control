######################################################
# Copyright (c) 2020 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# This code reads data from the MPU9250/MPU9265 board
# (MPU6050 - accel/gyro, AK8963 - mag) to verify its
# correct wiring to a Raspberry Pi and the functionality
# of the MPU9250_i2c.py library
#
#
######################################################
#
import time
t0 = time.time()
start_bool = False # boolean for connection
while (time.time()-t0)<5: # wait for 5-sec to connect to IMU
    try:
        from mpu9250_i2c import *
        start_bool = True # True for forthcoming loop
        break 
    except:
        continue
#
#############################
# Strings for Units/Labs
#############################
#
imu_devs   = ["ACCELEROMETER","GYROSCOPE"]
imu_labels = ["x-dir","y-dir","z-dir"]
imu_units  = ["g","g","g","dps","dps","dps"]
#
#############################
# Main Loop to Test IMU
#############################
ax2=0
while True:
    if start_bool==False: # make sure the IMU was started
        print("IMU not Started, Check Wiring") # check wiring if error
        break
    ##################################
    # Reading and Printing IMU values
    ##################################
    #
    try:
        ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
    except:
        continue 
    ax2=0
    #
    ##################################
    # Reading and Printing IMU values
    ##################################
    #
    for i in range(5):
        ax2 += ax

    ax2=ax2/5
    print(ax,', ' ,ax2)
   
    time.sleep(.05) # wait between prints