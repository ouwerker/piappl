# Author: Martin Ouwerkerk
# Version 1.0 20230628 
# License: MIT

import csv
import array as arr
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os.path

SENSORNAME=input('please enter the name of the sensor :\n')

datafile_path='/home/ouwerker/Data/'
complete_path=os.path.expanduser(datafile_path)

# default name_of_file='ADS1115output_2023-06-28_05'
part1_of_name=SENSORNAME+'output_'
part2_of_name='2023-06-28_17'
parts_of_name=part1_of_name+part2_of_name

complete_name=os.path.join(complete_path,SENSORNAME,parts_of_name+'.csv')
print(complete_name)
TIMEARRAY=arr.array('f')
VOLTAGEARRAY=arr.array('f')

# set plot parameters
fig, ax=plt.subplots(figsize=(7,3.8))
ax.set_xlabel('time [s]')
ax.set_ylabel('voltage [V]')

line_count = 0

with open(complete_name, newline='') as csvfile:
    fieldnames = ['time', 'voltage']
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)

    for row in reader:
        line_count +=1

# Omit the first header lines
        if line_count > 5:
            timefloat = float(row['time'])
            voltagefloat = float(row['voltage'])
#           print(timefloat,voltagefloat)
            TIMEARRAY.extend([timefloat])
            VOLTAGEARRAY.extend([voltagefloat])

ax.scatter(TIMEARRAY,VOLTAGEARRAY,marker='.', color='green')
plt.show()
plt.clf()
