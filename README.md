# Hovering Drone with PID Control

## Project Goal: Create a quadcopter that hovers

Problem: Hovering is difficult, especially for a human operator

Solution: Raspberry pi can control drone hover with high precision

Drone uses accelerometer, electronic speed controllers, motors, and RPI
RPI takes accelerometer data and adjusts speed of propellers

## Step 1: 
### Use Solidworks to design and print drone frame.

<img src="demo images/framecomponents.png" title="Frame Components">

<img src="demo images/droneframe.png" title="Frame Assembly">

Frame considerations: 

- replaceable wings (wings may break in the event of a crash)

- lightweight

- able to fit Raspberry Pi, accelerometer, and battery

## Step 2:
### PD Control Theory


<img src="demo images/dronepdgraph.png" title="PD Graph">

<img src="demo images/noisereduction.png" title="Noise Reduction">

<img src="demo images/pd raw inputs.png" title="PD Inputs">

<img src="demo images/assembly.jpg" title="Drone Assembly">
