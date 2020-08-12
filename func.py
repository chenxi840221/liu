# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# read wind data from csv file
# Choose 10-minute average or instantaneous
# output wind speed (knots)(6 decimal places) and meteorological direction
# tests
# Zipped GitHub project
# 

# %%
import pandas as pd


# %%
#get_ipython().system('ls')


# %%
line=[]
time=[]
speed=[]
direction=[]


# %%
import csv
import math

with open('sample.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} U(m/s) {row[1]}, v(m/s) {row[2]}.')
            line.append(row[0])
            time.append(row[0])
            speed.append(math.sqrt(math.pow(float(row[1]), 2) + math.pow(float(row[2]), 2)))
            direction.append(180/math.pi * (math.atan2(-float(row[1]),float(row[2]))))
            line_count += 1
    print(f'Processed {line_count} lines.')


# %%
download_dir = 'output.csv' #where you want the file to be downloaded to 
csv = open(download_dir, "w")
#"w" indicates that you're writing strings to the file
columnTitleRow = "datetime, WindSpeed, WindDir\n"
csv.write(columnTitleRow)
for i in range(len(time)):
    row=str(time[i])+","+str(speed[i])+","+str(direction[i])+"\n"
    print(row)
    csv.write(row)
csv.close()


# %%
idx = pd.date_range(time, periods=10, freq='min')

ts = pd.Series(range(len(idx)), index=idx)

ts
ts.resample('10min').mean()


# %%
time[1]


# %%



# %%



# %%



