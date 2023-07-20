# Author: Martin Ouwerkerk
# Version 1.0 20230720 
# License: MIT

import csv
import array as arr
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os.path

SENSORNAME='Acceleration'
#
# IMPORTANT:
# change the path to desired path
#
datafile_path='/home/ouwerker/Data/PiSenseHat/'
complete_path=os.path.expanduser(datafile_path)
#
# IMPORTANT:
# default name_of_file='Acceleration_2023-07-20_08' change to desired file name
#
part1_of_name=SENSORNAME+'_'
DATE = '2023-07-20'
NUMBER = '08'
part2_of_name = DATE + '_' + NUMBER
file_name=part1_of_name+part2_of_name
complete_name=os.path.join(complete_path,SENSORNAME,file_name+'.csv')

print(complete_name)

TIMEARRAY=arr.array('f')
XACCARRAY=arr.array('f')
YACCARRAY=arr.array('f')
ZACCARRAY=arr.array('f')

# set plot parameters
fig, ax=plt.subplots(figsize=(10,6))
ax.set_title(f'Pi Sense Hat {file_name}')
ax.set_xlabel('time [s]')
ax.set_ylabel('acceleration [g]')
line_count = 0

with open(complete_name, newline='') as csvfile:
    fieldnames = ['time', 'xacceleration', 'yacceleration', 'zacceleration']
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)

    for row in reader:
        line_count +=1

# Omit the first header lines
        if line_count > 5:
            timefloat = float(row['time'])
            xaccfloat = float(row['xacceleration'])
            yaccfloat = float(row['yacceleration'])
            zaccfloat = float(row['zacceleration'])
            TIMEARRAY.extend([timefloat])
            XACCARRAY.extend([xaccfloat])
            YACCARRAY.extend([yaccfloat])
            ZACCARRAY.extend([zaccfloat])

line1 = ax.scatter(TIMEARRAY,XACCARRAY,marker='.', color='green')
line2 = ax.scatter(TIMEARRAY,YACCARRAY,marker='.', color='red')
line3 = ax.scatter(TIMEARRAY,ZACCARRAY,marker='.', color='blue')
ax.legend([line1, line2, line3], ['x-acc', 'y-acc', 'z-acc'])
plt.show()
plt.clf()
