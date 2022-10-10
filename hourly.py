#This program grabs the hourly weather data for the time period of February 06, 2021 to February 24, 2021
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

#*******************HOURLY DATA*******************

#Get hourly data for time period
hourly_data = Hourly(san_antonio, start, end)

#Convert to Fahrenheit
hourly_data = hourly_data.convert(units.imperial)

#normalize data
hourly_data = hourly_data.normalize()

#Access the resulting DataFrame
hourly_data = hourly_data.fetch()
#print(hourly_data.head(5))

#create new data frame with data I want
refined_data = hourly_data.loc[:, 'temp']
#print(refined_data.head(5))

#*******************PLOTING HOURLY DATA*******************

#Using fivethirtyeight style for graph
plt.style.use("fivethirtyeight")

#plot the temperatures as a line graph
refined_data.plot(y=['temp'], color="blue", label="Temperature")
plt.ylim(0, 80)

#label axis and title
plt.xlabel("Date", labelpad=-20)
plt.ylabel("Temperature (°F)")
plt.title("San Antonio Hour by Hour Temperatures During the Texas Winter Storm")

#draw a line that represents freezing point 
plt.axline((0, 32), (24, 32), color="red", label="Freezing Point (32 °F)")

#show legend for readability
plt.legend(loc="upper center")

#annotate source
plt.annotate("Source: Meteostat.net; Raw data: NOAA, Deutscher Wetterdienst", (0,0), (750,-30), fontsize=12, 
             xycoords='axes fraction', textcoords='offset points', va='top')

#Display graph
plt.show()