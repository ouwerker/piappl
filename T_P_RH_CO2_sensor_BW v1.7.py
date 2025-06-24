# Author: Martin Ouwerkerk
# partly based on peppe80 code
# Version: 1.7 20250611
# battery percentage added since 1.2 20250604
# set auto calibration added since 1.3 20250606
# added partial refresh since 1.4 20250608
# added memory left bar and daily refresh since 1.5 20250611
# added daily clear and large font since 1.6 20250623
#
# License : MIT
# have these modules available in setup: writer, font24, ds3231_gen, scd4x_sensirion, bmp390, Pico ePaper 2.13 BW V4
# Tested to work with firmware pimoroni-picolipo_16mb-v1.21.0-micropython.uf2
#
import array
import os
import uos
import time
import utime
from machine import ADC, Pin, I2C, lightsleep
from pico_epaper import *
import framebuf
import bmp390
from scd4x_sensirion import SCD4xSensirion
from sensor_pack.bus_service import I2cAdapter
from ds3231_gen import *
import font24
from writer import Writer

def dt_tuple(dt):
    return time.localtime(time.mktime(dt))  # Populate weekday field

# set to correct sensor number between 1 and 99
sensornumber = 5

vsys = ADC(29)              # reads the system input voltage
charging = Pin(24, Pin.IN)  # reading GP24 tells us whether or not USB power is connected
conversion_factor = 3 * 3.3 / 65535
conversion_factorT = 3.3 / (65535)  # used for calculating a temperature from the raw sensor reading
voltagearray=array.array('f',[4.20,4.15,4.11,4.08,4.02,3.98,3.95,3.91,3.87,3.85,3.84,3.82,3.80,3.79,3.77,3.75,3.73,3.71,3.69,3.61,3.27])

sensor_temp = ADC(4)

listmem = uos.statvfs('/')
blocks_total = listmem[2]
blocks_left = listmem[3]
percentage_memory_left = 100 * blocks_left/blocks_total

# Please use the appropiate SDA and SCL pin numbers
i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=400000)

i2c_adaptor = I2C(id=0, scl=Pin(5, Pin.OPEN_DRAIN, value=2), sda=Pin(4), freq=400000)  # on Pimoroni Pi Pico Lipo RP2040 tested
adaptor = I2cAdapter(i2c_adaptor)

print("Martin's Pimoroni Pico Lipo with DS3231 RTC and SCD41 and BMP390 sensors")
print(adaptor)
print(i2c.scan())
print(i2c)
led = machine.Pin(23, machine.Pin.OUT)

# Create the RTC object using I2C
d = DS3231(i2c)
# dt = dt_tuple((2025, 6, 17, 22, 58, 2, 0, 0))
# d.set_time(dt)  # do this with correct time and date once after changing the battery

Datetimelist = d.get_time()
datum = f"{Datetimelist[0]:02d}-{Datetimelist[1]:02d}-{Datetimelist[2]:02d}"
startdatum = datum
tijd = f"{Datetimelist[3]:02d}:{Datetimelist[4]:02d}:{Datetimelist[5]:02d}"
starttijd = tijd

# convert the raw ADC read into a voltage
voltage = vsys.read_u16() * conversion_factor
j=0
percentage = 100
while voltage < voltagearray[j] and j<20:
    percentage = percentage - 5
    j+=1
strpercentage = f"{percentage:3d}"
strvoltage = f"{voltage:.3f}"
 
# Create the temperature and pressure sensor object using adaptor
tpsensor = bmp390.Bmp390(adaptor)
res = tpsensor.get_id()
print(f"chip_id: {res}")
calibration_data = [tpsensor.get_calibration_data(index) for index in range(0, 14)]
print(f"Calibration data: {calibration_data}")
print(f"Event: {tpsensor.get_event()}; Int status: {tpsensor.get_int_status()}; FIFO length: {tpsensor.get_fifo_length()}")
tpsensor.set_oversampling(2, 3)
tpsensor.set_sampling_period(5)
tpsensor.set_iir_filter(2)
tpsensor.start_measurement(True, True, 2)
s = tpsensor.get_status()
tBMP390 = 20
p = 101325.0
if s[2] and s[1]:
    tBMP390, p, tme = tpsensor.get_temperature(), tpsensor.get_pressure(), tpsensor.get_sensor_time()      

# Create the CO2, temperature and humidity sensor object using I2C
CO2sensor = SCD4xSensirion(adaptor)
CO2sensor.set_measurement(start=False, single_shot=False)
sid = CO2sensor.get_id()
print(f"Sensor id 3 x Word: {sid}")

# Warning: To change or read sensor settings, the SCD4x must be in idle mode!!!
# Otherwise an EIO exception will be raised!

# print(f"Set temperature offset sensor to {t_offs} Celsius")
t_offs = 0.0
CO2sensor.set_temperature_offset(t_offs)
t_offs = CO2sensor.get_temperature_offset()
print(f"Get temperature offset from sensor: {t_offs} Celsius")

# enter altitude above sea level in meters
masl = 0
print(f"Set my place M.A.S.L. to {masl} meter")
CO2sensor.set_altitude(masl)
masl = CO2sensor.get_altitude()
print(f"Get M.A.S.L. from sensor: {masl} meter")

# data ready
if CO2sensor.is_data_ready():
    print("Measurement data can be read!")
else:
    print("Measurement data missing!")
    
# Set auto calibration on (True)or off (False) here:
#CO2sensor.set_auto_calibration(False)

if CO2sensor.is_auto_calibration():
    print("The automatic self-calibration is ON!")
else:
    print("The automatic self-calibration is OFF!")
#    CO2sensor.set_auto_calibration(True)

# CO2sensor.set_measurement(start=False, single_shot=False)
wt = CO2sensor.get_conversion_cycle_time()

CO2sensor.set_measurement(start=False, single_shot=True, rht_only=False)
utime.sleep_ms(3 * wt)      # 3x period
co2, tSCD41, rh = CO2sensor.get_meas_data()


Tsensor1 = f"{tBMP390:.2f}"
Tsensor2 = f"{tSCD41:.2f}"
Hsensor = f"{rh:.1f}"
Psensor = f"{p:.1f}"
CO2value = f"{co2:4d}"

# Initialize the Raspberry PI Pico e-paper display
# Show static text
epd = EPD_2in13_V4_Portrait()
wri = Writer(epd, font24)

epd.init()
epd.Clear()    
epd.fill(0xff)
epd.text(datum, 20, 5, 0x00)
epd.text(tijd, 30, 20, 0x00)
epd.text("Martin's PicoPi", 0, 35, 0x00)
epd.text("Battery", 0, 50, 0x00)
epd.text(f"{strpercentage}%", 70, 50, 0x00)
epd.rect(0, 60, 100, 8, 0x00)
epd.fill_rect(0, 60, percentage, 8, 0x00)
epd.text(f"{Tsensor1}C", 10, 75, 0x00)
epd.text(f"{Tsensor2}C", 65, 75, 0x00)
epd.text(f" {Hsensor} %relHum", 10, 90, 0x00)
epd.text(f"{Psensor} Pa", 15, 105, 0x00)
epd.text("Carbon dioxide", 0, 120, 0x00)
Writer.set_textpos(epd, 130, 10)  # verbose = False to suppress console output
wri.printstring(f"{CO2value} ppm",invert=True)
epd.text(f"Batt. {strvoltage}V", 0, 160, 0x00)
epd.text("loopcount 0", 0, 175, 0x00)
epd.text("Elapsed    0 s", 0, 190, 0x00)
epd.text(f"Start {starttijd}", 0, 205, 0x00)
epd.text(f"     {startdatum}",0, 215, 0x00)
epd.text(f"Memory {percentage_memory_left:.1f}%", 0, 230, 0x00)
epd.text("Size", 0, 240, 0x00)
epd.display(epd.buffer)

# led = machine.Pin(23, machine.Pin.OUT)

# Generate data file name and file path
filenumber = 1
datafilename=f"{Datetimelist[0]:02d}{Datetimelist[1]:02d}{Datetimelist[2]:02d}_{filenumber:02d}_sensor{sensornumber:02d}.csv"
save_path=f"/Data/SCD41_BMP390"
print(save_path)
os.chdir(save_path)
fileinfo = os.ilistdir()
listnrexistingfile = -1
listnr = 1
for x in fileinfo:
    filename = x[0]
    if datafilename == filename:
        listnrexistingfile = listnr
    listnr += 1
listnr = 0
while listnrexistingfile > 0 :
    filenumber = filenumber+1
    datafilename = f"{Datetimelist[0]:02d}{Datetimelist[1]:02d}{Datetimelist[2]:02d}_{filenumber:02d}_sensor{sensornumber:02d}.csv"
    fileinfo = os.ilistdir()
    listnrexistingfile = -1
    listnr = 1
    for x in fileinfo:
        filename = x[0]
        if datafilename == filename:
            listnrexistingfile = listnr
        listnr += 1

print("sensor data is stored in: ",datafilename)
Datafile = open(datafilename,"w")
Datafile.write("date,time,temperature,temperature,humidity,pressure,CO2,voltage\n")
Datafile.write("YY-MM-DD,HH:MM:SS,degC,degC,%relHum,Pa,ppm,V\n")
Datafile.close()

# INTERVAL = 10

start = time.time()
elapsedtime = time.time() - start

loopcount = 1
while True:
    
    time.sleep(10)
#    led.on()
    
    # the following two lines do some maths to convert the number from the temp sensor into celsius
    reading = sensor_temp.read_u16() * conversion_factorT
    temperature = 33 - (reading - 0.706) / 0.001721
    Tsensor3 = f"{temperature:.2f}"

    epd.init()
    
    Datetimelist = d.get_time()
    datumNEW = f"{Datetimelist[0]:02d}-{Datetimelist[1]:02d}-{Datetimelist[2]:02d}"
    if datumNEW != datum:
        epd.Clear()   # once per day the epaper display needs to refresh completely
        epd.fill(0xff)
        time.sleep(2) # give it some extratime to settle
# all static information need to be witten again to the empty display
        epd.text(datumNEW, 20, 5, 0x00)
        epd.text(tijd, 30, 20, 0x00)
        epd.text("Martin's PicoPi", 0, 35, 0x00)
        epd.text("Battery", 0, 50, 0x00)
        epd.text(f"{strpercentage}%", 70, 50, 0x00)
        epd.rect(0, 60, 100, 8, 0x00)
        epd.fill_rect(0, 60, percentage, 8, 0x00)
        epd.text(f"{Tsensor1}C", 10, 75, 0x00)
        epd.text(f"{Tsensor2}C", 65, 75, 0x00)
        epd.text(f" {Hsensor} %relHum", 10, 90, 0x00)
        epd.text(f"{Psensor} Pa", 15, 105, 0x00)
        epd.text("Carbon dioxide", 0, 120, 0x00)
        Writer.set_textpos(epd, 130, 10)  # verbose = False to suppress console output
        wri.printstring(f"{CO2value} ppm",invert=True)
        epd.text(f"Batt. {strvoltage}V", 0, 160, 0x00)
        epd.text("loopcount", 0, 175, 0x00)
        epd.text(f"{loopcountstr}", 75, 175, 0x00)
        epd.text("Elapsed      s", 0, 190, 0x00)
        epd.text(f"{etimestr}", 70, 190, 0x00)        
        epd.text(f"Start {starttijd}", 0, 205, 0x00)
        epd.text(f"     {startdatum}",0, 215, 0x00)
        epd.text(f"Memory {percentage_memory_left:.1f}%", 0, 230, 0x00)
        epd.text("Size", 0, 240, 0x00)
        epd.text(f"{filesize}", 40, 240, 0x00)
        epd.display(epd.buffer)
        datum = datumNEW
        
    tijdNEW = f"{Datetimelist[3]:02d}:{Datetimelist[4]:02d}:{Datetimelist[5]:02d}"
    if tijdNEW != tijd:
        epd.fill_rect(30, 20, 90, 10, 0xff)
        epd.text(tijd, 30, 20, 0x00)        
        tijd = tijdNEW
        epd.displayPartial(epd.buffer)
        epd.delay_ms(100)

    s = tpsensor.get_status()
    if s[2] and s[1]:
        tBMP390, p, tme = tpsensor.get_temperature(), tpsensor.get_pressure(), tpsensor.get_sensor_time()
    else:
        print(f"Data ready: temp {s[2]}, press {s[1]}")
        continue        
    CO2sensor.set_measurement(start=False, single_shot=True, rht_only=False)
    utime.sleep_ms(3 * wt)      # 3x period
    co2, tSCD41, rh = CO2sensor.get_meas_data()

    elapsedtime = time.time() - start
    etimestr = str(elapsedtime)
    loopcountstr = str(loopcount)
        
# convert the raw ADC read into a voltage
    voltage = vsys.read_u16() * conversion_factor
    j=0
    percentage = 100
    while voltage < voltagearray[j] and j<20:
        percentage = percentage - 5
        j+=1

    print("percentage in loop:", percentage)

    strvoltageNEW = f"{voltage:.3f}"
    if strvoltageNEW != strvoltage:
        epd.fill_rect(48, 160, 60, 10, 0xff)
        epd.text(f"{strvoltageNEW}V", 60, 160, 0x00)
        strvoltage = strvoltageNEW              
        
    strpercentageNEW = f"{percentage:3d}"
    if strpercentageNEW != strpercentage:
        epd.fill_rect(70, 50, 40, 10, 0xff)
        epd.text(f"{strpercentageNEW}%", 70, 50, 0x00)
        epd.fill_rect(0, 60, 100, 8, 0xff)
        epd.fill_rect(0, 60, percentage, 8, 0x00)
        epd.rect(0, 60, 100, 8, 0x00)
        strpercentage = strpercentageNEW

    s = tpsensor.get_status()
    if s[2] and s[1]:
        tBMP390, p, tme = tpsensor.get_temperature(), tpsensor.get_pressure(), tpsensor.get_sensor_time()
    else:
        print(f"Data ready: temp {s[2]}, press {s[1]}")
        continue

    Tsensor1NEW = f"{tBMP390:.2f}"
    if Tsensor1NEW !=Tsensor1:
        epd.fill_rect(10, 75, 40, 10, 0xff)
        epd.text(f"{Tsensor1}", 10, 75, 0x00)
        Tsensor1 = Tsensor1NEW

    Tsensor2NEW = f"{tSCD41:.2f}"
    if Tsensor2NEW != Tsensor2:
        epd.fill_rect(65, 75, 40, 10, 0xff)
        epd.text(f"{Tsensor2}", 65, 75, 0x00)
        Tsensor2 = Tsensor2NEW

    HsensorNEW = f"{rh:.1f}"
    if HsensorNEW != Hsensor:
        epd.fill_rect(10, 90, 40, 10, 0xff)
        epd.text(f"{Hsensor}", 10, 90, 0x00)
        Hsensor = HsensorNEW
        
    PsensorNEW = f"{p:.1f}"
    if PsensorNEW != Psensor:
        epd.fill_rect(15, 105, 70, 10, 0xff)
        epd.text(f"{Psensor}", 15, 105, 0x00)
        Psensor = PsensorNEW

    CO2valueNEW = f"{co2:4d}"
    if CO2valueNEW != CO2value:
        epd.fill_rect(20,130,100,24, 0xff)
        Writer.set_textpos(epd, 130, 10)  # verbose = False to suppress console output
        wri.printstring(f"{CO2value} ppm",invert=True)
        CO2value = CO2valueNEW
        
    loopcountstr = str(loopcount)
    epd.fill_rect(75, 175, 40, 10, 0xff)
    epd.text(f"{loopcountstr}", 75, 175, 0x00)

    elapsedtime = time.time() - start
    etimestr = str(elapsedtime)
    epd.fill_rect(70, 190, 40, 10, 0xff)
    epd.text(f"{etimestr}", 70, 190, 0x00)

    Datafile=open(datafilename,"a")
    time.sleep(0.5)
    Datafile.write(datum+","+tijd+","+Tsensor1NEW+","+Tsensor2NEW+","+HsensorNEW+","+PsensorNEW+","+CO2valueNEW+","+strvoltageNEW+"\n")
    time.sleep(0.5)
    Datafile.close()
#    print(f"Voltage: {strvoltage} V Temperature: {Tsensor1} C {Tsensor2} C Humidity: {Hsensor} % Pressure: {Psensor} Pa CO2 {CO2value} ppm {tijd} {datum} elapsed {elapsedtime} s")

    fileinfo = os.ilistdir()
    for x in fileinfo:
        filesize = x[3]
    
    epd.fill_rect(40, 240, 80, 10, 0xff)
    epd.text(f"{filesize}", 40, 240, 0x00)

# memory bar
    listmem = uos.statvfs('/')
    blocks_left = listmem[3]
    percentage_memory_leftNEW = 100 * blocks_left/blocks_total
    if percentage_memory_leftNEW != percentage_memory_left:
        epd.fill_rect(50, 230, 50, 10, 0xff)
        epd.text(f"{percentage_memory_leftNEW:.1f} %", 60, 230, 0x00)
#        epd.fill_rect(00, 155, 100, 10, 0xff)
#        epd.rect(00,155,100,10,0x00)
        percentage_memory_left = percentage_memory_leftNEW

    epd.displayPartial(epd.buffer)

#    led.off()
    loopcount+=1    

epd.Clear()    
epd.fill(0xff)

print("End of program, goodbye!")


