# Author: Martin Ouwerkerk
# Version 1.320230729
# License: MIT

import csv
import array as arr
import matplotlib as mpl
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import os.path

SENSORNAME = 'AS7341'
SENSORMODALITY = 'Spectroscopy'
cwd = os.getcwd()
print(cwd)

datafile_path='/home/ouwerker/Data/' + SENSORNAME
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
WAVELENGTHARRAY=arr.array('f',[415.,445.,480.,515.,555.,590.,630.,680.])

INTENSITYARRAY_415=arr.array('f')
INTENSITYARRAY_445=arr.array('f')
INTENSITYARRAY_480=arr.array('f')
INTENSITYARRAY_515=arr.array('f')
INTENSITYARRAY_555=arr.array('f')
INTENSITYARRAY_590=arr.array('f')
INTENSITYARRAY_630=arr.array('f')
INTENSITYARRAY_680=arr.array('f')
INTENSITYARRAY_nearIR=arr.array('f')
INTENSITYARRAY_clear=arr.array('f')
WAVELENGTHARRAY_415=arr.array('f')
WAVELENGTHARRAY_445=arr.array('f')
WAVELENGTHARRAY_480=arr.array('f')
WAVELENGTHARRAY_515=arr.array('f')
WAVELENGTHARRAY_555=arr.array('f')
WAVELENGTHARRAY_590=arr.array('f')
WAVELENGTHARRAY_630=arr.array('f')
WAVELENGTHARRAY_680=arr.array('f')


# old 2D plot
# fig, ax=plt.subplots(figsize=(9,4.5))

ax = plt.figure().add_subplot(projection='3d')

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
ax.set_zlabel('light level [' + headeritems[1] + ']')
# use when a data unit is lacking in the data file
# ax.set_ylabel(fieldnames[1])
    
csvfile.close()

line_count = 0

with open(complete_name, newline='') as csvfile:
    fieldnames = ['time','415nm','445nm','480nm','515nm','555nm','590nm','630nm','680nm','nearIR','clear']
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)

    for row in reader:
        line_count +=1

# Omit the first header lines
        if line_count > 5:
            timefloat = float(row['time'])
            intensity_415_float = float(row['415nm'])
            intensity_445_float = float(row['445nm'])
            intensity_480_float = float(row['480nm'])
            intensity_515_float = float(row['515nm'])
            intensity_555_float = float(row['555nm'])
            intensity_590_float = float(row['590nm'])
            intensity_630_float = float(row['630nm'])
            intensity_680_float = float(row['680nm'])
            intensity_nearIR_float = float(row['nearIR'])
            intensity_clear_float  = float(row['clear'])
            TIMEARRAY.extend([timefloat])
            WAVELENGTHARRAY_415.extend([415.0])
            WAVELENGTHARRAY_445.extend([445.0])
            WAVELENGTHARRAY_480.extend([480.0])
            WAVELENGTHARRAY_515.extend([515.0])
            WAVELENGTHARRAY_555.extend([555.0])
            WAVELENGTHARRAY_590.extend([590.0])
            WAVELENGTHARRAY_630.extend([630.0])
            WAVELENGTHARRAY_680.extend([680.0])
            INTENSITYARRAY_415.extend([intensity_415_float])
            INTENSITYARRAY_445.extend([intensity_445_float])
            INTENSITYARRAY_480.extend([intensity_480_float])
            INTENSITYARRAY_515.extend([intensity_515_float])
            INTENSITYARRAY_555.extend([intensity_555_float])
            INTENSITYARRAY_590.extend([intensity_590_float])
            INTENSITYARRAY_630.extend([intensity_630_float])
            INTENSITYARRAY_680.extend([intensity_680_float])
            INTENSITYARRAY_nearIR.extend([intensity_nearIR_float])
            INTENSITYARRAY_clear.extend([intensity_clear_float])
XARRAY=np.row_stack((WAVELENGTHARRAY_415,WAVELENGTHARRAY_445,WAVELENGTHARRAY_480,WAVELENGTHARRAY_515,WAVELENGTHARRAY_555,WAVELENGTHARRAY_590,WAVELENGTHARRAY_630,WAVELENGTHARRAY_680)).T
YARRAY=np.row_stack((TIMEARRAY, TIMEARRAY, TIMEARRAY, TIMEARRAY, TIMEARRAY, TIMEARRAY, TIMEARRAY, TIMEARRAY)).T
ZARRAY=np.row_stack((INTENSITYARRAY_415, INTENSITYARRAY_445, INTENSITYARRAY_480, INTENSITYARRAY_515, INTENSITYARRAY_555, INTENSITYARRAY_590, INTENSITYARRAY_630, INTENSITYARRAY_680)).T
ZMAX = 2.0 * np.amax(ZARRAY)
R = int(line_count/50) + 2
ax.plot_surface(XARRAY, YARRAY, ZARRAY, cmap=cm.Blues, edgecolor = 'royalblue', lw = 0.5, rstride = R, cstride = 1)
ax.set(xlim=(400,700),ylim=(0,timefloat),zlim=(0,ZMAX),xlabel = 'wavelength [nm]',ylabel = 'time [s]',zlabel = 'intensity')

# line1 = ax.scatter(TIMEARRAY,INTENSITYARRAY_415,marker='.', color='purple')
# line2 = ax.scatter(TIMEARRAY,INTENSITYARRAY_445,marker='.', color='blue')
# line3 = ax.scatter(TIMEARRAY,INTENSITYARRAY_480,marker='.', color='green')
# line4 = ax.scatter(TIMEARRAY,INTENSITYARRAY_515,marker='.', color='yellow')
# line5 = ax.scatter(TIMEARRAY,INTENSITYARRAY_555,marker='.', color='orange')
# line6 = ax.scatter(TIMEARRAY,INTENSITYARRAY_590,marker='.', color='red')
# line7 = ax.scatter(TIMEARRAY,INTENSITYARRAY_630,marker='.', color='brown')
# line8 = ax.scatter(TIMEARRAY,INTENSITYARRAY_680,marker='.', color='black')
# ax.legend([line1,line2,line3,line4,line5,line6,line7,line8], ['415nm','445nm','480nm','515nm','555nm','590nm','630nm','680nm'])

plt.show()
plt.clf()

# Wrapping up
csvfile.close()
os.chdir(cwd)

