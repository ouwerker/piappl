# Author: Martin Ouwerkerk based on Adafruit_CircuitPython_AHTx0 driver
# Version 1.0 20230920 
# License: MIT

import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv

# Start of sensor specific part
MUNIT = 'microTesla'
MxUNIT = MUNIT
MyUNIT = MUNIT
MzUNIT = MUNIT
SENSORNAME = 'LIS3MDL'
SENSORMODALITY = 'magnetic_field'
import adafruit_lis3mdl
import board

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

sensor = adafruit_lis3mdl.LIS3MDL(i2c)

mag_x, mag_y, mag_z = sensor.magnetic

# End of sensor specific part

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
if REALTIMEGRAPH == 'Y' or REALTIMEGRAPH == 'y':
    GRAPHSENSOR = 'M'
GRAPHSENSOR = 'M'
# set plot parameters
PLOTTITLE = SENSORNAME + ' ' + SENSORMODALITY + ' sensor'
fig, ax=plt.subplots(figsize=(7.5,4.5))
ax.set_title(PLOTTITLE)
ax.set_xlabel('time ['+ TIMEUNIT + ']')
if GRAPHSENSOR == 'M':
    PLOTYLABEL = 'Magnetic field [' + MUNIT + ']'

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
    fieldnames = ['sensorname', 'magnetic_field_unit', 'duration', 'timeunit']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'sensorname': SENSORNAME, 'magnetic_field_unit': MUNIT, 'duration': DURATION, 'timeunit': TIMEUNIT})
    line_count += 1

print(f'{datetime.now().time()}\n')
print(f'Reading {SENSORNAME} for {DURATION:6d} seconds')
start = time.time()

import array as arr
TIMEARRAY=arr.array('f')
MAG_X_ARRAY=arr.array('f')
MAG_Y_ARRAY=arr.array('f')
MAG_Z_ARRAY=arr.array('f')

# Write header to csv file
with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['time', MxUNIT, MyUNIT, MzUNIT]
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_count += 1 

while (time.time() - start) <= DURATION:
    # Start of sensor specific part: read the sensor value and print it out.
    mag_x, mag_y, mag_z = sensor.magnetic
    # End of sensor specific part
    MAG_X_ARRAY.extend([mag_x])
    MAG_Y_ARRAY.extend([mag_y])
    MAG_Z_ARRAY.extend([mag_z])
    voortgang=time.time()-start
    TIMEARRAY.extend([voortgang])
 
    # Write sensor output to csv file
    with open(complete_name,'a', newline='') as csvfile:
        fieldnames = ['time', MxUNIT, MyUNIT, MzUNIT]
        line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        line_writer.writerow({'time': voortgang, MxUNIT: mag_x, MyUNIT: mag_y, MzUNIT: mag_z})
        line_count += 1
        
    print(f'Elapsed {voortgang:.1f} {TIMEUNIT} sensor {SENSORNAME}: x {mag_x:.1f}  y {mag_y:.1f}  z {mag_z:.1f} {MUNIT}')
        
    line1 = ax.scatter(TIMEARRAY,MAG_X_ARRAY,marker='.', color='green')
    line2 = ax.scatter(TIMEARRAY,MAG_Y_ARRAY,marker='.', color='blue')
    line3 = ax.scatter(TIMEARRAY,MAG_Z_ARRAY,marker='.', color='red')
    ax.legend([line1, line2, line3], ['x-mag', 'y-mag', 'z-mag'])
    
    # Show real time graph during interval
    if REALTIMEGRAPH == 'Y' or REALTIMEGRAPH == 'y': plt.pause(INTERVAL)
    else : time.sleep(INTERVAL)
    
# Show graph with end result
plt.show()
plt.clf()

# Wrapping up
csvfile.close()

