# Author: Martin Ouwerkerk based on Adafruit_CircuitPython_AHTx0 driver
# Version 1.0 20230811 
# License: MIT

import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv

# Start of sensor specific part
TUNIT = 'degC'
HUNIT = '%relHum'
SENSORNAME = 'AHT10'
SENSORMODALITY = 'temperature_humidity'
import adafruit_ahtx0
import board

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

sensor = adafruit_ahtx0.AHTx0(i2c)

TEMPERATURE = sensor.temperature
HUMIDITY = sensor.relative_humidity

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
    GRAPHSENSOR = input ('Temperature or relative humidity graph? T/H : ')
    while GRAPHSENSOR != 'T' and GRAPHSENSOR != 'H':
        GRAPHSENSOR = input ('invalid entry, please enter T for temperature of H for humidity : ')

# set plot parameters
PLOTTITLE = SENSORNAME + ' ' + SENSORMODALITY + ' sensor'
fig, ax=plt.subplots(figsize=(7,4.5))
ax.set_title(PLOTTITLE)
ax.set_xlabel('time ['+ TIMEUNIT + ']')
if GRAPHSENSOR == 'H':
    PLOTYLABEL = 'Relative humidity [' + HUNIT + ']'
if GRAPHSENSOR == 'T':
    PLOTYLABEL = 'Temperature [' + TUNIT + ']'

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
    fieldnames = ['sensorname', 'temperature_unit', 'humidity_unit', 'duration', 'timeunit']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'sensorname': SENSORNAME, 'temperature_unit': TUNIT, 'humidity_unit': HUNIT, 'duration': DURATION, 'timeunit': TIMEUNIT})
    line_count += 1

print(f'{datetime.now().time()}\n')
print(f'Reading {SENSORNAME} for {DURATION:6d} seconds')
start = time.time()

import array as arr
TIMEARRAY=arr.array('f')
TEMPERATUREARRAY=arr.array('f')
HUMIDITYARRAY=arr.array('f')

# Write header to csv file
with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['time', TUNIT, HUNIT]
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_count += 1 

while (time.time() - start) <= DURATION:
    # Start of sensor specific part: read the sensor value and print it out.
    TEMPERATURE = sensor.temperature
    HUMIDITY = sensor.relative_humidity
    # End of sensor specific part
    TEMPERATUREARRAY.extend([TEMPERATURE])
    HUMIDITYARRAY.extend([HUMIDITY])
    voortgang=time.time()-start
    TIMEARRAY.extend([voortgang])
 
    # Write sensor output to csv file
    with open(complete_name,'a', newline='') as csvfile:
        fieldnames = ['time', TUNIT, HUNIT]
        line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        line_writer.writerow({'time': voortgang, TUNIT: TEMPERATURE, HUNIT: HUMIDITY})
        line_count += 1
        
    print(f'Seconds since start {voortgang:.3f} sensor {SENSORNAME} reading {TEMPERATURE:.3f} {TUNIT} {HUMIDITY:.3f} {HUNIT}')
    if GRAPHSENSOR == 'H':
        ax.scatter(TIMEARRAY,HUMIDITYARRAY,marker='.', color='green')
    if GRAPHSENSOR == 'T':
        ax.scatter(TIMEARRAY,TEMPERATUREARRAY,marker='.', color='blue')
    # Show real time graph during interval
    if REALTIMEGRAPH == 'Y' or REALTIMEGRAPH == 'y': plt.pause(INTERVAL)
    else : time.sleep(INTERVAL)
    
# Show graph with end result
plt.show()
plt.clf()

# Wrapping up
csvfile.close()

