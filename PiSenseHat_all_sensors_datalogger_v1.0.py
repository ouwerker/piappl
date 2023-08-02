# Author: Martin Ouwerkerk based on Raspberry Pi Sense Hat example
# Version 3.3 20230731
# License: MIT

import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv

# Sensor specific part
A_UNIT = 'g'
H_UNIT = '%relHum'
L_UNIT = 'bit'
M_UNIT = 'micro Tesla'
P_UNIT = 'mBar'
T_UNIT = 'degC'
SENSORNAME = 'PiSenseHat'
SENSORMODALITY = 'All_sensors'

# specify timeunit
TIMEUNIT = 's'

# Generate data file name and file path
import datetime
import os.path
save_path='/home/ouwerker/Data/' + SENSORNAME + '/' + SENSORMODALITY + '/'
complete_path=os.path.expanduser(save_path)
if not os.path.exists(complete_path):
    os.makedirs(complete_path)
    print("Directory '%s' created successfully" %complete_path)

DATUM=str(datetime.date.today())
filenr = 1
filenrstr = str(filenr)
FILENUMBER='_0'+filenrstr
name_of_file=SENSORMODALITY + '_'
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
    name_of_file=SENSORMODALITY + '_'
    name_of_file=name_of_file+DATUM+FILENUMBER
    complete_name=os.path.join(complete_path,name_of_file+'.csv')
    EXISTS=os.path.exists(complete_name)
print(complete_name)

# Program the sensor
from sense_hat import SenseHat
sense = SenseHat()
sense.clear()

# Temperature section
thumcorrection = -3.3
tprecorrection = -1.2
Thum = sense.get_temperature_from_humidity() + thumcorrection
Tpre = sense.get_temperature_from_pressure() + tprecorrection

# Pressure section
pressurecorrection = -3.4
pressure = sense.get_pressure() + pressurecorrection

# Humidity section
humiditycorrection = 4.0
humidity = sense.get_humidity() + humiditycorrection

# Magnetometer section
magnetic_field = sense.get_compass_raw()
xmag = magnetic_field['x']
ymag = magnetic_field['y']
zmag = magnetic_field['z']

# Accelerometer section
xacccorrection=0.0
yacccorrection=0.0
zacccorrection=0.0
acceleration = sense.get_accelerometer_raw()
xacc = acceleration['x'] + xacccorrection
yacc = acceleration['y'] + yacccorrection
zacc = acceleration['z'] + zacccorrection

# Orientation section (not implemented yet)

# Colour section (not implemented yet)
sense.color.gain = 60
sense.color.integration_cycles = 64
time.sleep(2 * sense.colour.integration_time)
red, green, blue, clear = sense.colour.colour # readings scaled to 0-255

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
    fieldnames = ['sensorname','T-unit','T-unit','P-unit','H-unit','M-unit','M-unit','M-unit','A_UNIT','A_UNIT','A_UNIT','L_UNIT','duration','timeunit']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_writer.writerow({'sensorname':SENSORNAME,'T-unit':T_UNIT,'T-unit':T_UNIT,'P-unit':P_UNIT,'H-unit':H_UNIT,'M-unit':M_UNIT,'M-unit':M_UNIT,'M-unit':M_UNIT,'A_UNIT':A_UNIT,'A_UNIT':A_UNIT,'A_UNIT':A_UNIT,'L_UNIT':L_UNIT,'duration':DURATION,'timeunit':TIMEUNIT})
    line_count += 1

print(f'{datetime.now().time()}\n')
print(f'Reading {SENSORNAME} {SENSORMODALITY} for {DURATION:6d} seconds')
start = time.time()

# Arrays are needed for plotting a graph 
# import array as arr
# TIMEARRAY =arr.array('f')
# THUMARRAY =arr.array('f')
# TPREARRAY =arr.array('f')
# PRESSUREARRAY=arr.array('f')
# HUMIDITYARRAY=arr.array('f')
# XMAGARRAY=arr.array('f')
# YMAGARRAY=arr.array('f')
# ZMAGARRAY=arr.array('f')
# XACCARRAY=arr.array('f')
# YACCARRAY=arr.array('f')
# ZACCARRAY=arr.array('f')
# BLUEARRAY =arr.array('f')
# GREENARRAY=arr.array('f')
# REDARRAY  =arr.array('f')
# CLEARARRAY=arr.array('f')

# Write header to csv file
with open(complete_name,'a', newline='') as csvfile:
    fieldnames = ['time','Thum','Tpre','pressure','humidity','x_magnetic_field','y_magnetic_field','z_magnetic_field','xacceleration','yacceleration','zacceleration','light_level']
    line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    line_writer.writeheader()
    line_count += 1 

while (time.time() - start) <= DURATION:
    # Obtain data from the PiSenseHat sensors
    Thum = int(1000.0*(sense.get_temperature_from_humidity() + thumcorrection))
    Thum = Thum/1000.0
    Tpre = int(1000.0*(sense.get_temperature_from_pressure() + tprecorrection))
    Tpre = Tpre/1000.0
#    THUMARRAY.extend([Thum])
#    TPREARRAY.extend([Tpre])
    
    pressure = int(1000.0*(sense.get_pressure() + pressurecorrection))
    pressure = pressure/1000.0
#    PRESSUREARRAY.extend([pressure])

    humidity = int(1000.0*(sense.get_humidity() + humiditycorrection))
    humidity = humidity/1000.0
#    HUMIDITYARRAY.extend([humidity])
    
    magnetic_field = sense.get_compass_raw()
    xmag = int(1000.0*(magnetic_field['x']))
    ymag = int(1000.0*(magnetic_field['y']))
    zmag = int(1000.0*(magnetic_field['z']))
    xmag = xmag/1000.0
    ymag = ymag/1000.0
    zmag = zmag/1000.0
#    XMAGARRAY.extend(xmag)
#    YMAGARRAY.extend(ymag)
#    ZMAGARRAY.extend(zmag)

    xacccorrection=0.0
    yacccorrection=0.0
    zacccorrection=0.0
    acceleration = sense.get_accelerometer_raw()
    xacc = int(1000.0*(acceleration['x'] + xacccorrection))
    yacc = int(1000.0*(acceleration['y'] + yacccorrection))
    zacc = int(1000.0*(acceleration['z'] + zacccorrection))
    xacc = xacc/1000.0
    yacc = yacc/1000.0
    zacc = zacc/1000.0
#    XACCARRAY.extend(xacc)
#    YACCARRAY.extend(yacc)
#    ZACCARRAY.extend(zacc)
    time.sleep(2 * sense.colour.integration_time)
    red, green, blue, clear = sense.colour.colour # readings scaled to 0-255
    light_level = clear
    
    voortgang=int(1000.0*(time.time()-start))
    voortgang=voortgang/1000.0
    
#    TIMEARRAY.extend([voortgang])
 
    # Write sensor output to csv file
    with open(complete_name,'a', newline='') as csvfile:
        fieldnames = ['time','Thum','Tpre','pressure','humidity','x_magnetic_field','y_magnetic_field','z_magnetic_field','xacceleration','yacceleration','zacceleration','light_level']
        line_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        line_writer.writerow({'time':voortgang,'Thum': Thum,'Tpre':Tpre,'pressure':pressure,'humidity':humidity,'x_magnetic_field':xmag,'y_magnetic_field':ymag,'z_magnetic_field':zmag,'xacceleration':xacc,'yacceleration':yacc,'zacceleration':zacc,'light_level':light_level})
        line_count += 1
        
    print(f'Time {voortgang:.2f} {SENSORNAME} {SENSORMODALITY} {Tpre:.2f} {T_UNIT} {Thum:.2f} {T_UNIT} {pressure:.3f} {P_UNIT} {humidity:.1f} {H_UNIT} Magnetic xyz {xmag:.1f} {ymag:.1f} {zmag:.1f} {M_UNIT} Acc xyz {xacc:.3f} {yacc:.3f} {zacc:.3f} {A_UNIT} Light {light_level:3d} {L_UNIT}')

    time.sleep(INTERVAL)

# Wrapping up
sense.clear()
csvfile.close()

