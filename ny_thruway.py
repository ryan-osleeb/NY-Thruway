#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.ny.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.ny.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
#2020 Data
results = client.get("r8tn-bjyq", limit=4724503)
#2019 Data
#results = client.get("chzq-388p", limit=1000000)

# Convert to pandas DataFrame
ny_thruway = pd.DataFrame.from_records(results)

#Save to csv file
ny_thruway.to_csv('ny_car_data_2020.csv', index=False)

ny_thruway_cars = ny_thruway[['date', 'vehicle_count']]
ny_thruway_cars['vehicle_count'] = ny_thruway_cars['vehicle_count'].astype(str).astype(int)
ny_thruway_cars['date'] = pd.to_datetime(ny_thruway_cars['date'])
ny_cars = ny_thruway_cars.groupby(['date']).sum()

plt.plot(ny_cars)
plt.show()