# Author: Martin Ouwerkerk based on Raspberry Pi Sense Hat example
# Version 1.0 20230731
# License: MIT

import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv

# Sensor specific
UNIT = 'bit'
SENSORNAME = 'PiSenseHat'
SENSORMODALITY = 'Colour'

# specify timeunit
TIMEUNIT = 's'

# set plot parameters
PLOTTITLE = SENSORNAME + ' ' + SENSORMODALITY + ' sensor'
fig, ax=plt.subplots(figsize=(7,4.5))
ax.set_title(PLOTTITLE)
ax.set_xlabel('time [' + TIMEUNIT + ']')
ax.set_ylabel('colour [' + UNIT + ']')

# Generate data file name and file path
import datetime
import os.path
save_path='/home/ouwerker/Data/' + SENSORNAME + '/' + SENSORMODALITY + '/'
complete_path=os.path.expanduser(save_path)
if not os.path.exists(complete_path):
    os.makedirs(complete_path)
    print("Directory '%s' created successfully" %complete_path)
DATUM=str(datetime.date.today())
filenr = 1
filenrstr = str(filenr)
FILENUMBER='_0'+filenrstr
name_of_file = SENSORMODALITY + '_'
name_of_file=name_of_file + DATUM + FILENUMBER
complete_name=os.path.join(complete_path,name_of_file+'.csv')
EXISTS=os.path.exists(complete_name)
while  EXISTS :
    filenr=filenr+1
    filenrstr=str(filenr)
    if filenr < 10 :
        FILENUMBER='_0'+filenrstr
    else :
        FILENUMBER='_'+filenrstr
    name_of_file = SENSORMODALITY + '_'
    name_of_file = name_of_file + DATUM + FILENUMBER
    complete_name=os.path.join(complete_path,name_of_file+'.csv')
    EXISTS=os.path.exists(complete_name)
print('Data is written in csv format to this location:')
print(complete_name)
print()

# Program the Pi Sense Hat
from sense_hat import SenseHat
sense = SenseHat()
sense.clear()

sense.color.gain = 60
sense.color.integration_cycles = 64

time.sleep(2 * sense.colour.integration_time)
red, green, blue, clear = sense.colour.colour # readings scaled to 0-256
print(f"R: {red}, G: {green}, B: {blue}, C: {clear}")


# setting axes limits
print('Sensor data is shown in a graph')
plotrange = 255
plotrange = float(plotrange)

bottom = 0.0
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

with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['sensorname', 'unit', 'duration', 'timeunit']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'sensorname': SENSORNAME, 'unit': UNIT, 'duration': DURATION, 'timeunit': TIMEUNIT})
    line_count += 1

print(f'Data collection starts at: {datetime.now().time()}\n')
print(f'Reading {SENSORNAME} {SENSORMODALITY} in {UNIT} for {DURATION:6d} seconds')
start = time.time()

import array as arr
TIMEARRAY =arr.array('f')
BLUEARRAY =arr.array('f')
GREENARRAY=arr.array('f')
REDARRAY  =arr.array('f')
CLEARARRAY=arr.array('f')

# Write header to csv file
with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['time', 'blue', 'green', 'red', 'clear']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_count += 1 

while (time.time() - start) <= DURATION:
    # Read the colour values and print it out.
    
    time.sleep(2 * sense.colour.integration_time)
    red, green, blue, clear = sense.colour.colour # readings scaled to 0-256
    print(f"R: {red}, G: {green}, B: {blue}, C: {clear}")
    
    BLUEARRAY.extend([blue])
    GREENARRAY.extend([green])
    REDARRAY.extend([red])
    CLEARARRAY.extend([clear])
    voortgang=time.time()-start
    TIMEARRAY.extend([voortgang])
 
    # Write sensor output to csv file
    with open(complete_name,'a', newline='') as csvfile:
        fieldnames = ['time', 'blue', 'green', 'red', 'clear']
        line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        line_writer.writerow({'time': voortgang, 'blue': blue, 'green': green, 'red': red, 'clear': clear})
        line_count += 1
        
    print(f'Time {voortgang:.3f} s  Colour: blue {blue:3d} {UNIT}  green {green:3d} {UNIT}  red {red:3d} {UNIT}  clear {clear:3d} {UNIT}')
    
    line1 = ax.scatter(TIMEARRAY,BLUEARRAY,marker='.', color='blue')
    line2 = ax.scatter(TIMEARRAY,GREENARRAY,marker='.', color='green')
    line3 = ax.scatter(TIMEARRAY,REDARRAY,marker='.', color='red')
    line4 = ax.scatter(TIMEARRAY,CLEARARRAY,marker='.', color='grey')
    ax.legend([line1, line2, line3, line4], ['blue', 'green', 'red', 'clear'])
 
    # Show real time graph during interval
    if REALTIMEGRAPH == 'Y' or REALTIMEGRAPH == 'y': plt.pause(INTERVAL)
    else : time.sleep(INTERVAL)
    
# Show graph with end result
plt.show()
plt.clf()

# Wrapping up
sense.clear()
csvfile.close()
