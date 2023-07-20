# Author: Martin Ouwerkerk based on Raspberry Pi Sense Hat example
# Version 3.3 20230720 
# License: MIT
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
# from matplotlib.markers import MarkerStyle
import numpy as np
import csv

# set plot parameters

fig, ax=plt.subplots(figsize=(7,4.5))
ax.set_title('Acceleration')
ax.set_xlabel('time [s]')
ax.set_ylabel('acceleration [g]')

# marker_style=dict(markersize=10, markerfacecolor='tab:blue',markeredgecolor='tab:red')
# Generate data file name and file path

import datetime
import os.path
save_path='/home/ouwerker/Data/PiSenseHat/Acceleration/'
complete_path=os.path.expanduser(save_path)
DATUM=str(datetime.date.today())
filenr = 1
filenrstr = str(filenr)
FILENUMBER='_0'+filenrstr
name_of_file='Acceleration_'
name_of_file=name_of_file+DATUM+FILENUMBER
complete_name=os.path.join(complete_path,name_of_file+'.csv')
EXISTS=os.path.exists(complete_name)
while  EXISTS :
    filenr=filenr+1
    filenrstr=str(filenr)
    if filenr < 10 :
        FILENUMBER='_0'+filenrstr
    else :
        FILENUMBER='_'+filenrstr
    name_of_file='Acceleration_'
    name_of_file=name_of_file+DATUM+FILENUMBER
    complete_name=os.path.join(complete_path,name_of_file+'.csv')
    EXISTS=os.path.exists(complete_name)
print('Data is written in csv format to this location:')
print(complete_name)
print()

# Program the Pi Sense Hat
from sense_hat import SenseHat
sense = SenseHat()
sense.clear()

acccorrection=0.0
acceleration = sense.get_accelerometer_raw()

xacc = acceleration['x']-acccorrection
yacc = acceleration['y']-acccorrection
zacc = acceleration['z']-acccorrection

# setting axes limits
print('Sensor data is shown in a graph')
plotrange = input('please enter g range of y-axis (0.1...8):\n')
plotrange = float(plotrange)
while plotrange < 0.1 or plotrange > 8.0:
    plotrange = input('invalid entry, please enter g range of y-axis (0.1...8) :\n')
    plotrange = float(plotrange)
    
plotrange = float(plotrange)
bottom = -1.0*plotrange
top    = plotrange
ax.set_ylim(bottom,top)

from datetime import datetime

# Choose measurement interval 
INTERVAL = input('please enter data collection interval in milliseconds :\n')
INTERVAL=float(INTERVAL)
while INTERVAL < 1 :
    INTERVAL = input('value out of range, please enter a positive interval value of 1 or more:\n')
    INTERVAL = float(INTERVAL)

INTERVAL=INTERVAL/1000

# Choose duration of data collection
DURATION = input('please enter data collection duration in seconds :\n')
DURATION = int(DURATION)
while DURATION < 1 :
    DURATION = input('invalid entry, please enter a duration value of 1 or more :\n')
    DURATION = int(DURATION) 

# Choose real time graph of data or only at end of data collection
print('A plot of the obtained data is always shown at the end of data collection')
REALTIMEGRAPH = input('do you wish a real time plot? (slows down data collection considerably) Y/N  ')

# Write settings to csv file
line_count = 0
STARTTIME = datetime.now().time()

with open(complete_name,'w', newline='') as csvfile:
    fieldnames = ['startdate', 'starttime']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'startdate': DATUM, 'starttime': STARTTIME})
    line_count += 1

SENSORUNIT = 'g'

with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['unit', 'duration in seconds']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'unit': SENSORUNIT, 'duration in seconds': DURATION})
    line_count += 1

print(f'Data collection starts at: {datetime.now().time()}\n')
print(f'Reading PiSenseHat acceleration in {SENSORUNIT} for {DURATION:6d} seconds')
start = time.time()

import array as arr
TIMEARRAY=arr.array('f')
XACCARRAY=arr.array('f')
YACCARRAY=arr.array('f')
ZACCARRAY=arr.array('f')

# Write header to csv file
with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['time', 'xacceleration', 'yacceleration', 'zacceleration']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_count += 1 

while (time.time() - start) <= DURATION:
    # Read the acceleration values and print it out.
    acceleration = sense.get_accelerometer_raw()

    xacc = acceleration['x']-acccorrection
    yacc = acceleration['y']-acccorrection
    zacc = acceleration['z']-acccorrection

    XACCARRAY.extend([xacc])
    YACCARRAY.extend([yacc])
    ZACCARRAY.extend([zacc])
    voortgang=time.time()-start
    TIMEARRAY.extend([voortgang])
 
    # Write sensor output to csv file
    with open(complete_name,'a', newline='') as csvfile:
        fieldnames = ['time', 'xacceleration', 'yacceleration', 'zacceleration']
        line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        line_writer.writerow({'time': voortgang, 'xacceleration': xacc, 'yacceleration': yacc, 'zacceleration': zacc})
        line_count += 1
        
    print(f'Time since start {voortgang:.3f} s  Acceleration: x {xacc:.4f} {SENSORUNIT}  y {yacc:.4f} {SENSORUNIT}  z {zacc:.4f} {SENSORUNIT}')
    
    
    line1 = ax.scatter(TIMEARRAY,XACCARRAY,marker='.', color='green')
    line2 = ax.scatter(TIMEARRAY,YACCARRAY,marker='.', color='red')
    line3 = ax.scatter(TIMEARRAY,ZACCARRAY,marker='.', color='blue')
    ax.legend([line1, line2, line3], ['x-acc', 'y-acc', 'z-acc'])
 
    # Show real time graph during interval
    if REALTIMEGRAPH == 'Y' or REALTIMEGRAPH == 'y': plt.pause(INTERVAL)
    else : time.sleep(INTERVAL)
    
# Show graph with end result
plt.show()
plt.clf()
