# Author: Martin Ouwerkerk based on Raspberry Pi Sense Hat example
# Version 3.3 20230731
# License: MIT

import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv

# Sensor specific part
UNIT = 'degC'
SENSORNAME = 'PiSenseHat'
SENSORMODALITY = 'Temperature'

# specify timeunit
TIMEUNIT = 's'

# marker_style=dict(markersize=10, markerfacecolor='tab:blue',markeredgecolor='tab:red')
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
name_of_file=SENSORMODALITY + '_'
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
    name_of_file=SENSORMODALITY + '_'
    name_of_file=name_of_file+DATUM+FILENUMBER
    complete_name=os.path.join(complete_path,name_of_file+'.csv')
    EXISTS=os.path.exists(complete_name)
print(complete_name)

# set plot parameters
PLOTTITLE = SENSORNAME + ' ' + SENSORMODALITY + ' sensor'
fig, ax=plt.subplots(figsize=(7,4.5))
ax.set_title(PLOTTITLE)
ax.set_xlabel('time ['+ TIMEUNIT + ']')
PLOTYLABEL = SENSORMODALITY + ' [' + UNIT + ']'
ax.set_ylabel(PLOTYLABEL)

# Program the sensor
from sense_hat import SenseHat
sense = SenseHat()
# calibrate the sensors with a reliable sensor and enter the correction below
thumcorrection = -3.3
tprecorrection = -1.2
# Tcor = sense.get_temperature() + temperaturecorrection
Thum = sense.get_temperature_from_humidity() + thumcorrection
Tpre = sense.get_temperature_from_pressure() + tprecorrection

# get a second reading tot make sure it is not a zero reading (PiSenseHat bug..)
time.sleep(1)
# Tcor = sense.get_temperature() + temperaturecorrection
Thum = sense.get_temperature_from_humidity() + thumcorrection
Tpre = sense.get_temperature_from_pressure() + tprecorrection

value = Tpre

# setting axes limits narrowed to a range
plotrange = input('please enter desired range of y-axis :\n')
intplotrange = int(plotrange)
halfplotrange = intplotrange/2
intvalue=int(value)
bottom =intvalue-halfplotrange
top=intvalue+halfplotrange

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

with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['sensorname', 'unit', 'duration', 'timeunit']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'sensorname': SENSORNAME, 'unit': UNIT, 'duration': DURATION, 'timeunit': TIMEUNIT})
    line_count += 1

print(f'{datetime.now().time()}\n')
print(f'Reading {SENSORNAME} {SENSORMODALITY} in {UNIT} for {DURATION:6d} seconds')
start = time.time()

import array as arr
TIMEARRAY=arr.array('f')
# TCORARRAY=arr.array('f')
THUMARRAY=arr.array('f')
TPREARRAY=arr.array('f')

# Write header to csv file
with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['time', 'temperature']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_count += 1 

while (time.time() - start) <= DURATION:
    # Read the sensor value
    # Tcor = sense.get_temperature() + temperaturecorrection
    Thum = sense.get_temperature_from_humidity() + thumcorrection
    Tpre = sense.get_temperature_from_pressure() + tprecorrection

#   TCORARRAY.extend([Tcor])
    THUMARRAY.extend([Thum])
    TPREARRAY.extend([Tpre])
    voortgang=time.time()-start
    TIMEARRAY.extend([voortgang])
 
    # Write sensor output to csv file
    with open(complete_name,'a', newline='') as csvfile:
        fieldnames = ['time', 'Thum', 'Tpre']
        line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        line_writer.writerow({'time': voortgang, 'Thum': Thum, 'Tpre': Tpre})
        line_count += 1
        
    print(f'Seconds {voortgang:.3f} {SENSORNAME} {SENSORMODALITY} {Tpre:.3f} {UNIT} and {Thum:.3f} {UNIT}')
#    line1 = ax.scatter(TIMEARRAY,TCORARRAY,marker='.', color='green')
    line1 = ax.scatter(TIMEARRAY,THUMARRAY,marker='.', color='blue')
    line2 = ax.scatter(TIMEARRAY,TPREARRAY,marker='.', color='red')
    
    ax.legend([line1, line2], ['T humidity', 'T pressure'])

    # Show real time graph during interval
    if REALTIMEGRAPH == 'Y' or REALTIMEGRAPH == 'y': plt.pause(INTERVAL)
    else : time.sleep(INTERVAL)

# Show graph with end result
plt.show()
plt.clf()

# Wrapping up
sense.clear()
csvfile.close()

