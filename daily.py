#This program grabs the daily weather data for the time period of February 06, 2021 to February 24, 2021
#using the Meteostat library

from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
from meteostat import Point, Daily, Hourly, units
import pandas as pd
import numpy as np
from collections import Counter

#Set start and end dates
start = datetime(2021, 2, 6)
end = datetime(2021, 2, 24)

#Creating point for San Antonio, TX
san_antonio = Point(29.4243, -98.4911)

#*******************DAILY DATA*******************

#Get daily data for time period
daily_data = Daily(san_antonio, start, end)

#convert to imperial units
daily_data = daily_data.convert(units.imperial)

#normalize data
daily_data = daily_data.normalize()

#access the resulting DataFrame
daily_data = daily_data.fetch()

#drop unnecessary columns
daily_data = daily_data.drop(["wpgt", "pres", "wdir","tsun"], axis=1)

#rename columns to be more readable
daily_data = daily_data.rename(columns={"tavg": "Avg Temperature", "tmin": "Min Temperature", "tmax": "Max Temperature", "prcp": "Precipitation", "snow": "Snow (in)", "wspd": "Wind Speed"})

#calculating wind chill temperature(Avg Temperature - (windspeed * 0.7))
wind_chill = []
for wind in daily_data["Wind Speed"]: #get wind chill list
    wind_chill.append(wind * 0.7)

#calculate wind chill temperature for min and max temps
min_wind_chill_temps = []
max_wind_chill_temps = []

i = 0
for temp in daily_data["Min Temperature"]:
    min_wind_chill_temps.append(temp - wind_chill[i])
    i += 1

i = 0
for temp in daily_data["Max Temperature"]:
    max_wind_chill_temps.append(temp - wind_chill[i])
    i += 1

#add column to dataframe with wind chill temperature
daily_data['Wind Chill'] = wind_chill
daily_data['Min Wind Chill Temperature'] = min_wind_chill_temps
daily_data['Max Wind Chill Temperature'] = max_wind_chill_temps
print(daily_data)

#Using fivethirtyeight style for graph
plt.style.use("fivethirtyeight")

#plot the temperatures as a line graph
plt.plot(daily_data["Min Temperature"], color="#0000FF", label="Minimum Temperature")
#plt.plot(daily_data["Max Temperature"], color="#4B0082", label="Max Temperature")
plt.plot(daily_data["Min Wind Chill Temperature"], color="#00FFFF", label="Minimum Wind Chill Temperature (Feels Like)")
#plt.plot(daily_data["Max Wind Chill Temperature"], color="#9370DB", label="Max Wind Chill Temperature (Feels Like)")

#label axis and title
plt.xlabel("Date")
plt.ylabel("Temperature (°F)")
plt.title("How Cold Did It Get and How Cold Did It Feel?")

#draw a line that represents freezing point 
#plt.axline((0, 32), (24, 32), color="red", label="Freezing Point (32 °F)")

#show legend for readability
plt.legend(loc="upper center")

#annotate source
plt.annotate("Source: Meteostat.net; Raw data: NOAA, Deutscher Wetterdienst", (0,0), (750, -100), fontsize=12, 
             xycoords='axes fraction', textcoords='offset points', va='top')


#format dates
plt.gcf().autofmt_xdate()
date_format = mpl_dates.DateFormatter("%b %d, %Y") #Month Day, Year
plt.gca().xaxis.set_major_formatter(date_format) #sets the format
plt.gca().xaxis.set_major_locator(mpl_dates.DayLocator(interval=1)) #sets interval to daily

#Display graph
plt.show()

plt.figure(2)

#Using fivethirtyeight style for graph
plt.style.use("fivethirtyeight")

#using bar graph
plt.plot(daily_data["Snow (in)"], color="#0000FF")

#Labels and source
plt.xlabel("Date")
plt.ylabel("Snow (inches)")
plt.title("San Antonio Daily Snowfall During the Texas Winter Storm")
plt.annotate("Source: Meteostat.net; Raw data: NOAA, Deutscher Wetterdienst", (0,0), (750, -100), fontsize=12, 
             xycoords='axes fraction', textcoords='offset points', va='top')

#format dates
plt.gcf().autofmt_xdate()
date_format = mpl_dates.DateFormatter("%b %d, %Y") #Month Day, Year
plt.gca().xaxis.set_major_formatter(date_format) #sets the format
plt.gca().xaxis.set_major_locator(mpl_dates.DayLocator(interval=1)) #sets interval to daily

#display
plt.show()