# Author: Martin Ouwerkerk
# Version 1.0 20250304
# License: MIT

# !!!!!  prior to running this program run: sudo pigpiod
# !!!!!  prior to running this program run: sudo apt install python3-pyqt6
# !!!!!  prior to running this program run: sudo apt install python3-matplotlib

import time
import pigpio
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv

# Start of sensor specific part
FREQUNIT = 'Hz'
SENSORNAME = 'Egely Wheel'
SENSORMODALITY = 'pulse frequency'
RISING_EDGE = 0

# Connect the red wire of the Egely Wheel to GPIO 4 (pin7) and black to GND (pin6)
GPIO = 4
pi= pigpio.pi('soft',8888) 
cb = pi.callback(GPIO,edge=RISING_EDGE,func=None)
    
# specify timeunit
TIMEUNIT = 's'

# Generate data file name and file path
import datetime
import os.path
save_path='/home/ouwerker/Data/' + SENSORNAME + '/'
complete_path=os.path.expanduser(save_path)
if not os.path.exists(complete_path):
    os.makedirs(complete_path)
    print("Directory '%s' created successfully" %SENSORNAME)

DATUM=str(datetime.date.today())
filenr = 1
filenrstr = str(filenr)
FILENUMBER='_0'+filenrstr
name_of_file=SENSORNAME + 'output_'
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
    name_of_file = SENSORNAME +'output_'
    name_of_file=name_of_file+DATUM+FILENUMBER
    complete_name=os.path.join(complete_path,name_of_file+'.csv')
    EXISTS=os.path.exists(complete_name)
print(complete_name)

# Choose measurement interval 

INTERVAL=1.0

# Choose duration of data collection
DURATION = input('please enter duration in seconds :\n')
DURATION = int(DURATION)
while DURATION < 1 :
    DURATION = input('invalid entry, please enter a duration value of 1 or more :\n')
    DURATION = int(DURATION) 

# Choose real time graph of data or only at end of data collection
REALTIMEGRAPH = input('real time graph? Y/N  ')

# set plot parameters
PLOTTITLE = SENSORNAME + ' ' + SENSORMODALITY + ' sensor'
fig, ax=plt.subplots(figsize=(7,4.5))
ax.set_title(PLOTTITLE)
ax.set_xlabel('time ['+ TIMEUNIT + ']')
PLOTYLABEL = 'Pulse frequency [' + FREQUNIT + ']'
ax.set_ylabel(PLOTYLABEL)


# Write settings to csv file
line_count = 0
from datetime import datetime
STARTTIME = datetime.now().time()

with open(complete_name,'w', newline='') as csvfile:
    fieldnames = ['startdate', 'starttime']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'startdate': DATUM, 'starttime': STARTTIME})
    line_count += 1

with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['sensorname', 'frequency_unit', 'duration', 'timeunit']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'sensorname': SENSORNAME, 'frequency_unit': FREQUNIT, 'duration': DURATION, 'timeunit': TIMEUNIT})
    line_count += 1

print(f'{datetime.now().time()}\n')
print(f'Reading {SENSORNAME} for {DURATION:6d} seconds')
start = time.time()

import array as arr
TIMEARRAY=arr.array('f')
FREQARRAY=arr.array('f')

# Write header to csv file
with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['time', FREQUNIT]
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_count += 1 
cbcountold = 0
while (time.time() - start) <= DURATION:
    # Start of sensor specific part: read the sensor value and print it out.
    # to achieve Hz use 100 and to achieve the Egely Wheel reading use 120 below
    Pulsespersecond = (cb.count/120)-cbcountold
    FREQUENCY = Pulsespersecond
    cbcountold = cb.count/120
    
    # End of sensor specific part
    FREQARRAY.extend([FREQUENCY])
    
    voortgang=time.time()-start
    TIMEARRAY.extend([voortgang])
 
    # Write sensor output to csv file
    with open(complete_name,'a', newline='') as csvfile:
        fieldnames = ['time', FREQUNIT]
        line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        line_writer.writerow({'time': voortgang, FREQUNIT: FREQUENCY})
        line_count += 1
        
    print(f'Seconds since start {voortgang:.3f} sensor {SENSORNAME} reading {FREQUENCY:.3f} {FREQUNIT}')
    
    ax.scatter(TIMEARRAY,FREQARRAY,marker='.', color='green')
    
    print('tot hier')
    
    if REALTIMEGRAPH == 'Y' or REALTIMEGRAPH == 'y': plt.pause(INTERVAL)
    else : time.sleep(INTERVAL)
    
# Show graph with end result
plt.show()
plt.clf()

# Wrapping up
csvfile.close()

