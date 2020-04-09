import sqlite3
import sys
import Adafruit_DHT

sensorId = Adafruit_DHT.DHT11
sensorPin = 19

def log_values(sensor_id, temp, hum):
	conn=sqlite3.connect('/var/www/web_app/weatherApp.db')  #It is important to provide an
							     #absolute path to the database
							     #file, otherwise Cron won't be
							     #able to find it!
	# For the time-related code (record timestamps and time-date calculations) to work 
	# correctly, it is important to ensure that your Raspberry Pi is set to UTC.
	# This is done by default!
	# In general, servers are assumed to be in UTC.
	curs=conn.cursor()
	curs.execute("""INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,temp))
	curs.execute("""INSERT INTO humidity values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,hum))
	conn.commit()
	conn.close()

humidity, temperature = Adafruit_DHT.read_retry(sensorId, sensorPin)
# If you don't have a sensor but still wish to run this program, comment out all the 
# sensor related lines, and uncomment the following lines (these will produce random
# numbers for the temperature and humidity variables):
# import random
# humidity = random.randint(1,100)
# temperature = random.randint(10,30)
if humidity is not None and temperature is not None:
	log_values("1", temperature, humidity)	
else:
	log_values("1", -999, -999)
