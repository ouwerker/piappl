# Author: Martin Ouwerkerk based on discontinued Adafruit_ADS1x15 example
# Version 1.0 20230724 
# License: MIT

import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv

# Start of sensor specific part
UNITLIST = ['ppm', 'ppb']
SENSORNAME = 'SGP30'
SENSORMODALITYLIST = ['CO2','TVOC']

# specify timeunit
TIMEUNIT = 's'

# set plot parameters
PLOTTITLE = SENSORNAME + ' ' + UNITLIST[1] + ' sensor'
fig, ax=plt.subplots(figsize=(7,4.5))
ax.set_title(PLOTTITLE)
ax.set_xlabel('time ['+ TIMEUNIT + ']')
PLOTYLABEL = SENSORMODALITYLIST[1] + ' [' + UNITLIST[1] + ']'
ax.set_ylabel(PLOTYLABEL)

# Generate data file name and file path
import datetime
import os.path
save_path='/home/ouwerker/Data/'+ SENSORNAME + '/'
complete_path=os.path.expanduser(save_path)
if not os.path.exists(complete_path):
    os.makedirs(complete_path)
    print("Directory '%s' created successfully" %SENSORNAME)

DATUM=str(datetime.date.today())
filenr = 1
filenrstr = str(filenr)
FILENUMBER='_0'+filenrstr
name_of_file=SENSORNAME+'output_'
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
    name_of_file=SENSORNAME +'output_'
    name_of_file=name_of_file+DATUM+FILENUMBER
    complete_name=os.path.join(complete_path,name_of_file+'.csv')
    EXISTS=os.path.exists(complete_name)
print(complete_name)


# Program the sensor
import board
import busio
import adafruit_sgp30

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.set_iaq_baseline(0x8973, 0x8AAE)

# Estimate! Best to measure T and relHum% and use these values
sgp30.set_iaq_relative_humidity(celsius=22.1, relative_humidity=44)

SENSOROUTPUTCO2 = sgp.eCO2
SENSOROUTPUTTVOC = sgp30.TVOC
BASELINECO2 = sgp30.baseline_eCO2
BASELINETVOC = sgp30.baseline_TVOC

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
    line_writer.writerow({'sensorname': SENSORNAME, 'units': UNITLIST, 'duration': DURATION, 'timeunit': TIMEUNIT})
    line_count += 1


print(f'{datetime.now().time()}\n')
print(f'Reading {SENSORNAME} for {DURATION:6d} seconds')
start = time.time()

import array as arr
TIMEARRAY=arr.array('f')
SENSOROUTPUTCO2ARRAY=arr.array('f')
SENSOROUTPUTTVOCARRAY=arr.array('f')

# Write header to csv file
with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['time', 'CO2', 'TVOC']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_count += 1 

while (time.time() - start) <= DURATION:
    # Read the SGP30 output
    SENSOROUTPUTCO2 = sgp.eCO2
    SENSOROUTPUTTVOC = sgp30.TVOC
    BASELINECO2 = sgp30.baseline_eCO2
    BASELINETVOC = sgp30.baseline_TVOC
    SENSOROUTPUTCO2ARRAY.extend([SENSOROUTPUTCO2])
    SENSOROUTPUTTVOCARRAY.extend([SENSOROUTPUTTVOC])
    voortgang=time.time()-start
    TIMEARRAY.extend([voortgang])
 
    # Write sensor output to csv file
    with open(complete_name,'a', newline='') as csvfile:
        fieldnames = ['time', UNIT]
        line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        line_writer.writerow({'time': voortgang, UNIT: value})
        line_count += 1

    print(f' {voortgang:.3f} {TIMEUNIT}  {SENSORMODALITYLIST[1]} {SENSOROUTPUTCO2:4d} {UNITLIST[1]} and {SENSORMODALITYLIST[1]} {SENSOROUTPUTTVOC:4d} {UNITLIST[2]}')
    ax.scatter(TIMEARRAY,SENSOROUTPUTCO2ARRAY,marker='.', color='blue')
    ax.scatter(TIMEARRAY,SENSOROUTPUTTVOCARRAY,marker='.', color='green')
    # Show real time graph during interval
    if REALTIMEGRAPH == 'Y' or REALTIMEGRAPH == 'y': plt.pause(INTERVAL)
    else : time.sleep(INTERVAL)
    
# Show graph with end result
plt.show()
plt.clf()

# Wrapping up
csvfile.close()
