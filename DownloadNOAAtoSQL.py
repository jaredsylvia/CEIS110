#Purpose: Build weather database from NOAA data
#Name: Jared Sylvia
#Date: 3/16/2021
#   See https://pypi.org/project/noaa-sdk/ for details on noaa_sdk package used
# Original script supplied for coursework, this one has been modified to use MySQL instead of SQLite

from noaa_sdk import noaa
import mysql.connector
import datetime

# parameters for retrieving NOAA weather data
zipCode = "95355"  # change to your postal code
country = "US" 
mySQLuser = 'ceis110'         #added for MySQL authentication, change to your own
mySQLpass = 'ceis110'
#date-time format is yyyy-mm-ddThh:mm:ssZ, times are Zulu time (GMT)
#gets the most recent 14 days of data
today = datetime.datetime.now()
past = today - datetime.timedelta(days=14)
startDate = past.strftime("%Y-%m-%dT00:00:00Z") 
endDate = today.strftime("%Y-%m-%dT23:59:59Z") 

#create connect/ion - this creates database if not exist
print("Preparing database...")
conn = mysql.connector.connect(user=mySQLuser, password=mySQLpass, host='127.0.0.1', database='ceis110')
#create cursor to execute SQL commands
cur = conn.cursor()

#drop previous version of table if any so we start fresh each time
dropTableCmd = "DROP TABLE IF EXISTS observations;"
cur.execute(dropTableCmd)

#create new table to store observations
createTableCmd = """ CREATE TABLE IF NOT EXISTS observations (            
                        timestamp VARCHAR(31) NOT NULL PRIMARY KEY,             
                        windSpeed FLOAT,                                        
                        temperature FLOAT,
                        relativeHumidity FLOAT,
                        windDirection INTEGER,
                        barometricPressure INTEGER,
                        visibility INTEGER,
                        textDescription TEXT
                     ) ; """  #changed to VARCHAR to set key length for MySQL/MariaDB, changed REAL to FLOAT to adhere more accurately to MariaDB standards
cur.execute(createTableCmd)
print("Database prepared")

# Get hourly weather observations from NOAA Weather Service API
print("Getting weather data...")
n = noaa.NOAA()
observations =  n.get_observations(zipCode,country,startDate,endDate)

#populate table with weather observations
print("Inserting rows...")
insertCmd = """ INSERT INTO observations 
                    (timestamp, windSpeed, temperature, relativeHumidity, 
                     windDirection, barometricPressure, visibility, textDescription)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s) """                       #changed ? to %s to fit MySQL/MariaDB standards
count = 0
for obs in observations:
    insertValues = (obs["timestamp"],
                    obs["windSpeed"]["value"],
                    obs["temperature"]["value"],
                    obs["relativeHumidity"]["value"],
                    obs["windDirection"]["value"],
                    obs["barometricPressure"]["value"],
                    obs["visibility"]["value"],
                    obs["textDescription"])
    cur.execute(insertCmd, insertValues)
    count += 1
if count > 0:
    cur.execute("COMMIT;")
print(count, "rows inserted")
print("Database load complete!")

