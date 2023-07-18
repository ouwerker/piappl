# Author: Martin Ouwerkerk based on Adafruit example
# Version 3.1 20230628 
# License: Public Domain
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
# from matplotlib.markers import MarkerStyle
import numpy as np
import csv

# set plot parameters

fig, ax=plt.subplots(figsize=(7,4.5))
ax.set_title('ADS1115')
ax.set_xlabel('time [s]')
ax.set_ylabel('voltage [V]')
# marker_style=dict(markersize=10, markerfacecolor='tab:blue',markeredgecolor='tab:red')
# Generate data file name and file path

import datetime
import os.path
save_path='/home/ouwerker/Data/ADS1115/'
complete_path=os.path.expanduser(save_path)
DATUM=str(datetime.date.today())
filenr = 1
filenrstr = str(filenr)
FILENUMBER='_0'+filenrstr
name_of_file='ADS1115output_'
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
    name_of_file='ADS1115output_'
    name_of_file=name_of_file+DATUM+FILENUMBER
    complete_name=os.path.join(complete_path,name_of_file+'.csv')
    EXISTS=os.path.exists(complete_name)
print(complete_name)


# Program the Adafruit ADS1115 4-channel 16-bit ADC module

import Adafruit_ADS1x15
from datetime import datetime
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

print('Pick a gain to choose the range of voltages that are read:\n - 1 = +/-4.096V\n - 2 = +/-2.048V\n - 4 = +/-1.024V\n - 8 = +/-0.512V\n -16 = +/-0.256V\n')
GAIN=input('please enter the gain :\n')
if GAIN=='2/3' : 
    GAINFLOAT = 0.66667
else :
    GAINFLOAT =float(GAIN)

VRANGE=4.096/GAINFLOAT
# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.

# Choose ADS1115 input channel (0..3)
CHANNEL = input('please enter channel (0..3):\n')
CHANNEL = int(CHANNEL)
while CHANNEL > 3 or CHANNEL < 0 :
    CHANNEL = input('channel out of range (0..3) please try again:\n')
    CHANNEL = int(CHANNEL)

# Choose measurement interval 
INTERVAL = input('please enter interval in milliseconds :\n')
INTERVAL=float(INTERVAL)
while INTERVAL < 1 :
    INTERVAL = input('value out of range, please enter a positive interval value of 1 or more:\n')
    INTERVAL = float(INTERVAL)

# adjust default sampling rate (128Hz) when interval too short
if INTERVAL < 8: 
    DATARATE = 860
else : 
    DATARATE = 128
INTERVAL=INTERVAL/1000

# Choose duration of data collection
DURATION = input('please enter duration in seconds :\n')
DURATION = int(DURATION)
while DURATION < 1 :
    DURATION = input('invalid entry, please enter a duration value of 1 or more :\n')
    DURATION = int(DURATION) 

# Choose real time graph of data or only at end of data collection
REALTIMEGRAPH = input('real time graph? Y/N  ')

# Start continuous ADC conversions on channel 0 using the previously set gain
# value.  Note you can also pass an optional data_rate parameter, see the simpletest.py
# example and read_adc function for more information.
if GAINFLOAT < 1 :
    adc.start_adc(channel=CHANNEL, gain=2/3, data_rate=DATARATE)
else :
    GAIN=int(GAIN)
    adc.start_adc(channel=CHANNEL, gain=GAIN, data_rate=DATARATE)
# Once continuous ADC conversions are started you can call get_last_result() to
# retrieve the latest result, or stop_adc() to stop conversions.

# Note you can also call start_adc_difference() to take continuous differential
# readings.  See the read_adc_difference() function in differential.py for more
# information and parameter description.

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
    fieldnames = ['gain', 'channel', 'duration']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'gain': GAIN, 'channel': CHANNEL, 'duration': DURATION})
    line_count += 1

print(f'{datetime.now().time()}\n')
print(f'Reading ADS1115 channel {CHANNEL:1d} with gain {GAIN} and voltage range +/- {VRANGE:.3f} for {DURATION:6d} seconds')
start = time.time()

import array as arr
TIMEARRAY=arr.array('f')
VOLTAGEARRAY=arr.array('f')

# Write header to csv file
with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['time', 'voltage']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_count += 1 

while (time.time() - start) <= DURATION:
    # Read the last ADC conversion value and print it out.
    value = adc.get_last_result()
    voltage=VRANGE*value/32768
    VOLTAGEARRAY.extend([voltage])
    voortgang=time.time()-start
    TIMEARRAY.extend([voortgang])
 
    # Write sensor output to csv file
    with open(complete_name,'a', newline='') as csvfile:
        fieldnames = ['time', 'voltage']
        line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        line_writer.writerow({'time': voortgang, 'voltage': voltage})
        line_count += 1
        
    # WARNING! If you try to read any other ADC channel during this continuous
    # conversion (like by calling read_adc again) it will disable the
    # continuous conversion!
    print(f'Channel {CHANNEL:1d}: {voortgang:.3f} {value:6d} {voltage:.4f}')
    ax.scatter(TIMEARRAY,VOLTAGEARRAY,marker='.', color='green')
    # Show real time graph during interval
    if REALTIMEGRAPH == 'Y' or REALTIMEGRAPH == 'y': plt.pause(INTERVAL)
    else : time.sleep(INTERVAL)
    
# Stop continuous conversion.  After this point you can't get data from get_last_result!
adc.stop_adc()

# Show graph with end result
plt.show()
plt.clf()
