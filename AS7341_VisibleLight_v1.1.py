# Author: Martin Ouwerkerk
# Version 1.1 202306030
# License: MIT

import time
from time import sleep
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime
import os.path
import board
import adafruit_as7341
from adafruit_as7341 import AS7341
import array as arr

# Prepare graph
fig, ax=plt.subplots(figsize=(7,4.5))

# Generate data file name and file path
save_path='/home/ouwerker/Data/AS7341/'
complete_path=os.path.expanduser(save_path)
DATUM=str(datetime.date.today())
filenr = 1
filenrstr = str(filenr)
FILENUMBER='_0'+filenrstr
name_of_file='AS7341output_'
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
    name_of_file='AS7341output_'
    name_of_file=name_of_file+DATUM+FILENUMBER
    complete_name=os.path.join(complete_path,name_of_file+'.csv')
    EXISTS=os.path.exists(complete_name)
print(complete_name)

# Prepare I2C interface
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = AS7341(i2c)

TIMEARRAY=arr.array('f')
WAVELENGTHARRAY=arr.array('d')
WAVELENGTHARRAY=([415,445,480,515,555,590,630,680])
INTENSITYARRAY=arr.array('f')

# Choose measurement interval
INTERVAL = input('please enter sampling interval in milliseconds (1300 or more) :\n')
INTERVAL=float(INTERVAL)
while INTERVAL < 1300 :
    INTERVAL = input('value out of range, please enter a positive interval value of 1300 or more:\n')
    INTERVAL = float(INTERVAL)
INTERVAL=INTERVAL-1300
if INTERVAL < 0 : INTERVAL=1
INTERVAL=INTERVAL/1000

# Choose duration of data collection
DURATION = input('please enter duration in seconds :\n')
DURATION = int(DURATION)
while DURATION < 1 :
    DURATION = input('invalid entry, please enter a duration value of 1 or more :\n')
    DURATION = int(DURATION) 

# Choice for illumination with white LED
sensor.led_current = 10
LEDCHOICE = input('Activate LED? (Y/N) :\n')
if LEDCHOICE =='Y' or LEDCHOICE=='y': sensor.led = True

# Choose real time graph of data or only data collection
REALTIMEGRAPH = input('real time graph? Y/N : ')

from datetime import datetime
print(f'{datetime.now().time()}\n')
STARTTIME = datetime.now().time()
print(f'Reading AS7341 for {DURATION:6d} seconds')
start = time.time()
line_count = 0

with open(complete_name,'w', newline='') as csvfile:
    
    fieldnames = ['startdate', 'starttime']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'startdate': DATUM, 'starttime': STARTTIME})
    line_count += 1
    
with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['time', '415nm', '445nm', '480nm', '515nm', '555nm', '590nm', '630nm', '680nm', 'nearIR', 'clear' ]
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_count += 1
        
while (time.time() - start) <= DURATION:
    voortgang=time.time()-start
    TIMEARRAY.extend([voortgang])
    INTENSITYARRAY=([sensor.channel_415nm,sensor.channel_445nm,sensor.channel_480nm,sensor.channel_515nm,sensor.channel_555nm,sensor.channel_590nm,sensor.channel_630nm,sensor.channel_680nm])
    ax.plot(WAVELENGTHARRAY,INTENSITYARRAY)
    print(f'elapsed time since start [s]: {voortgang:.3f}')
    
    # Write sensor output to csv file
    with open(complete_name,'a', newline='') as csvfile:
        fieldnames = ['time', '415nm', '445nm', '480nm', '515nm', '555nm', '590nm', '630nm', '680nm', 'nearIR', 'clear' ]
        line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        line_writer.writerow({'time':voortgang,'415nm':sensor.channel_415nm,'445nm':sensor.channel_445nm,'480nm':sensor.channel_480nm,'515nm':sensor.channel_515nm,'555nm':sensor.channel_555nm,'590nm':sensor.channel_590nm,'630nm':sensor.channel_630nm,'680nm':sensor.channel_680nm,'nearIR':sensor.channel_nir,'clear':sensor.channel_clear})
        line_count += 1
 
    # Sleep during interval
    if REALTIMEGRAPH == 'Y' or REALTIMEGRAPH == 'y': plt.pause(INTERVAL)
    else : time.sleep(INTERVAL)
    
   
# Wrapping up
sensor.led = False
plt.show()
plt.clf()
