# Author: Martin Ouwerkerk based on Raspberry Pi Sense Hat example
# Version 3.2 20230719 
# License: MIT
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
# from matplotlib.markers import MarkerStyle
import numpy as np
import csv

# set plot parameters

fig, ax=plt.subplots(figsize=(7,4.5))
ax.set_title('Pressure')
ax.set_xlabel('time [s]')
ax.set_ylabel('pressure [mBar]')

# marker_style=dict(markersize=10, markerfacecolor='tab:blue',markeredgecolor='tab:red')
# Generate data file name and file path

import datetime
import os.path
save_path='/home/ouwerker/Data/PiSenseHat/Pressure/'
complete_path=os.path.expanduser(save_path)
DATUM=str(datetime.date.today())
filenr = 1
filenrstr = str(filenr)
FILENUMBER='_0'+filenrstr
name_of_file='Pressure_'
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
    name_of_file='Pressure_'
    name_of_file=name_of_file+DATUM+FILENUMBER
    complete_name=os.path.join(complete_path,name_of_file+'.csv')
    EXISTS=os.path.exists(complete_name)
print(complete_name)


# Program the Pi Sense Hat

from sense_hat import SenseHat
sense = SenseHat()
sense.clear()
pressure = sense.get_pressure()


# setting axes limits narrowed to 1 mbar range
plotrange = input('please enter pressure range of y-axis :\n')
intplotrange = int(plotrange)
halfplotrange = intplotrange/2
intpressure=int(pressure)
bottom =intpressure-halfplotrange
top=intpressure+halfplotrange

ax.set_ylim(bottom,top)

from datetime import datetime

# Choose measurement interval 
INTERVAL = input('please enter interval in milliseconds :\n')
INTERVAL=float(INTERVAL)
while INTERVAL < 1 :
    INTERVAL = input('value out of range, please enter a positive interval value of 1 or more:\n')
    INTERVAL = float(INTERVAL)

INTERVAL=INTERVAL/1000

# Choose duration of data collection
DURATION = input('please enter duration in seconds :\n')
DURATION = int(DURATION)
while DURATION < 1 :
    DURATION = input('invalid entry, please enter a duration value of 1 or more :\n')
    DURATION = int(DURATION) 

# Choose real time graph of data or only at end of data collection
REALTIMEGRAPH = input('real time graph? Y/N  ')


# Write settings to csv file
line_count = 0
STARTTIME = datetime.now().time()

with open(complete_name,'w', newline='') as csvfile:
    fieldnames = ['startdate', 'starttime']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'startdate': DATUM, 'starttime': STARTTIME})
    line_count += 1

PRESSUREUNIT = 'mBar'

with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['pressureunit', 'duration']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'pressureunit': PRESSUREUNIT, 'duration': DURATION})
    line_count += 1

print(f'{datetime.now().time()}\n')
print(f'Reading PiSenseHat pressure in {PRESSUREUNIT} for {DURATION:6d} seconds')
start = time.time()

import array as arr
TIMEARRAY=arr.array('f')
PRESSUREARRAY=arr.array('f')

# Write header to csv file
with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['time', 'pressure']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_count += 1 

while (time.time() - start) <= DURATION:
    # Read the pressure value and print it out.
    pressure = sense.get_pressure()

    PRESSUREARRAY.extend([pressure])
    voortgang=time.time()-start
    TIMEARRAY.extend([voortgang])
 
    # Write sensor output to csv file
    with open(complete_name,'a', newline='') as csvfile:
        fieldnames = ['time', 'pressure']
        line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        line_writer.writerow({'time': voortgang, 'pressure': pressure})
        line_count += 1
        
 
    print(f'Pressure {pressure:.4f} {PRESSUREUNIT} at {voortgang:.3f} seconds after start of data collection')
    ax.scatter(TIMEARRAY,PRESSUREARRAY,marker='.', color='green')
    # Show real time graph during interval
    if REALTIMEGRAPH == 'Y' or REALTIMEGRAPH == 'y': plt.pause(INTERVAL)
    else : time.sleep(INTERVAL)
    

# Show graph with end result
plt.show()
plt.clf()
