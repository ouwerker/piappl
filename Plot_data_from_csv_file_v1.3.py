# Author: Martin Ouwerkerk
# Version 1.3 20230819
# License: MIT

import csv
import array as arr
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os

cwd = os.getcwd()
print(cwd)

SENSORNAME=input('Please enter the sensor name (enter for PiSenseHat/Sensormodality):\n')

datafile_path='/home/ouwerker/Data/'+SENSORNAME
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
SENSOROUTPUTARRAY=arr.array('f')

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
            print(fieldnames)
            
Last = len(headeritems)-1

DATASETNAME=input('Please enter a dataset name from above list:\n')

while not DATASETNAME in fieldnames:
    DATASETNAME=input('Name not found, please enter a valid dataset name:\n')
    
Dataset = fieldnames.index(DATASETNAME)

# Dataset = 1

# set plot parameters, uncomment what is applicable
# use when a time unit is present in the data file
ax.set_xlabel(fieldnames[0] + ' [' + headeritems[Last] + ']')
# use when a time unit is lacking in the data file
# ax.set_xlabel(fieldnames[0])
# use when a data unit is present in the data file
ax.set_ylabel(fieldnames[Dataset] + ' [' + headeritems[Dataset] + ']')
# use when a data unit is lacking in the data file
# ax.set_ylabel(fieldnames[1])
    
csvfile.close()

# start reading data file again with DictReader
line_count = 0
with open(complete_name, newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)
    for row in reader:
        line_count +=1
        if line_count>5:
            timefloat = float(row[fieldnames[0]])
            sensoroutputfloat = float(row[fieldnames[Dataset]])
            # print(timefloat,sensoroutputfloat)
            TIMEARRAY.extend([timefloat])
            SENSOROUTPUTARRAY.extend([sensoroutputfloat])

# generate graph
ax.scatter(TIMEARRAY,SENSOROUTPUTARRAY,marker='.', color='green')
plt.show()
plt.clf()

# Wrapping up
csvfile.close()
os.chdir(cwd)




