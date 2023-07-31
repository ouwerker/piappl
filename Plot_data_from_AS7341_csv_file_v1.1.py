# Author: Martin Ouwerkerk
# Version 1.1 20230724 
# License: MIT

import csv
import array as arr
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os.path

SENSORNAME = 'PiSenseHat'
SENSORMODALITY = 'Acceleration'
cwd = os.getcwd()
print(cwd)

datafile_path='/home/ouwerker/Data/' + SENSORNAME + '/' + SENSORMODALITY 
print(f'Data files for this sensor can be found here: {datafile_path}')

while not os.path.exists(datafile_path):
    SENSORNAME=input('Name not found, please enter a valid sensor name:\n')
    datafile_path='/home/ouwerker/Data/'+SENSORNAME
    
os.chdir(datafile_path)
cwdnew = os.getcwd()
print(cwdnew)

from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()
complete_name = askopenfilename()

print(complete_name)

TIMEARRAY=arr.array('f')
XACCARRAY=arr.array('f')
YACCARRAY=arr.array('f')
ZACCARRAY=arr.array('f')

fig, ax=plt.subplots(figsize=(9,4.5))
line_count = 0

with open(complete_name, newline='') as csvfile:
    heading1=next(csvfile)
    heading2=SENSORNAME + ' data starting ' + next(csvfile)
    # generate plot title, removing all decimals from time stamp
    ax.set_title(heading2[:-9])
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        line_count +=1
        if line_count==1:
            headernames = row
        if line_count==2:
            headeritems = row
        if line_count==3:
            fieldnames = row
            
# set plot parameters, uncomment what is applicable
# use when a time unit is present in the data file
ax.set_xlabel(fieldnames[0] + ' [' + headeritems[3] + ']')
# use when a time unit is lacking in the data file
# ax.set_xlabel(fieldnames[0])
# use when a data unit is present in the data file
ax.set_ylabel(fieldnames[1] + ' [' + headeritems[1] + ']')
# use when a data unit is lacking in the data file
# ax.set_ylabel(fieldnames[1])
    
csvfile.close()

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

# Wrapping up
csvfile.close()
os.chdir(cwd)

