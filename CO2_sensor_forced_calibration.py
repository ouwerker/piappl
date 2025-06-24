# Author: Martin Ouwerkerk
# Version: 1.0
# License : MIT

# have these modules available in your raspberry pi pico
import time
import utime
from machine import ADC, Pin, I2C, lightsleep
import framebuf
from scd4x_sensirion import SCD4xSensirion
from sensor_pack.bus_service import I2cAdapter

i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=400000)

i2c_adaptor = I2C(id=0, scl=Pin(5, Pin.OPEN_DRAIN, value=2), sda=Pin(4), freq=400000)  # on Pimoroni Pi Pico Lipo RP2040 tested
adaptor = I2cAdapter(i2c_adaptor)

print("Martin's Pimoroni Pico Lipo with SCD41 sensor")
print(adaptor)
print(i2c.scan())
print(i2c)
led = machine.Pin(23, machine.Pin.OUT)

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

time.sleep(30)

# enter CO2 level for forced recalibration
CO2level = 780


CO2sensor.force_recalibration(CO2level)

time.sleep(30)

# data ready
if CO2sensor.is_data_ready():
    print("Measurement data can be read!")
else:
    print("Measurement data missing!")
    
if CO2sensor.is_auto_calibration():
    print("The automatic self-calibration is ON!")
else:
    print("The automatic self-calibration is OFF!")

# CO2sensor.set_measurement(start=False, single_shot=False)
wt = CO2sensor.get_conversion_cycle_time()

led = machine.Pin(23, machine.Pin.OUT)

led.on()
     
CO2sensor.set_measurement(start=False, single_shot=True, rht_only=False)
utime.sleep_ms(3 * wt)      # 3x period
co2, tSCD41, rh = CO2sensor.get_meas_data()
CO2value = f"{co2:4d}"

print(f" CO2 {CO2value} ppm")

print("End of program, goodbye!")

