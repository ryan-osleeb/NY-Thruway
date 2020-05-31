import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#download files
file_folder = '/Users/rosleeb/ny_thruway'
data_2019 = pd.read_csv(f'{file_folder}/ny_thruway_data_2019.csv')
data_2020 = pd.read_csv(f'{file_folder}/ny_car_data_2020.csv')
eia_gas_demand = pd.read_csv(f'{file_folder}/eia_gas_demand.csv')

#daily 2019 data
ny_cars_2019 = data_2019[['Date', 'Vehicle Count']]
ny_cars_2019['Vehicle Count'] = ny_cars_2019['Vehicle Count'].astype(str).astype(int)
ny_cars_2019['Date'] = pd.to_datetime(ny_cars_2019['Date'])
cars_2019 = ny_cars_2019.groupby(['Date']).sum()

#daily 2020 data
ny_cars_2020 = data_2020[['Date', 'Vehicle Count']]
ny_cars_2020['Vehicle Count'] = ny_cars_2020['Vehicle Count'].astype(str).astype(int)
ny_cars_2020['Date'] = pd.to_datetime(ny_cars_2020['Date'])
cars_2020 = ny_cars_2020.groupby(['Date']).sum()

#plot 2020 data
plt.figure(figsize=(13, 8))
sns.set(style="darkgrid")
sns.lineplot(data=cars_2020['Vehicle Count'], palette="tab10", linewidth=2.5).set_title("2020 NY Cars on Road")
plt.show()

#get rolling averages
average_2019 = []
for i in range(len(cars_2019['Vehicle Count'])):
    avg = np.average(cars_2019['Vehicle Count'][i:i+7])
    average_2019.append(avg)

cars_2019 = cars_2019.assign(avg = average_2019)

average_2020 = []
for i in range(len(cars_2020['Vehicle Count'])):
    avg = np.average(cars_2020['Vehicle Count'][i:i+7])
    average_2020.append(avg)
    
cars_2020 = cars_2020.assign(avg = average_2020)

#plot rolling averages
plt.figure(figsize=(8, 5))
sns.set(style="darkgrid")
sns.lineplot(data=np.array(average_2019), palette="tab10", linewidth=2.5).set_title("NY Cars on Road")
sns.lineplot(data=np.array(average_2020[:147]), palette="tab10", linewidth=2.5).set_title("NY Cars on Road")
plt.show()

#plot year-on-year change
yoy_change = (np.array(average_2020[:149])-np.array(average_2019[:149]))/np.array(average_2019[:149])
plt.plot(yoy_change[:147])
plt.title("Year-on-year Change in NY Cars")
plt.show()

cars_on_road = cars_2019
cars_on_road = cars_on_road.append(cars_2020)

cars_eia = []
for i in range(72):
    cars_eia.append(cars_on_road['avg'][i*7].astype(float))
cars_eia.append(cars_on_road['avg'][-1:][0])
cars_matrix = eia_gas_demand.assign(cars = cars_eia)

fig, ax1 = plt.subplots()
ax1.plot(cars_matrix['cars'])
ax2 = ax1.twinx()
ax2.plot(cars_matrix['Gasoline Demand'])
plt.title("NY Cars on Road (LHS) vs EIA Gasoline Demand (RHS)")
plt.show()

