import math
from readdata import *
import pandas as pd

def time_convert(time):
# convert the format of time strings to YYYY-MM-DD HH:MM:SS
        timestamp=[]
        for i in range(len(time)):
                Year=int(time[i][0]+time[i][1]+time[i][2]+time[i][3])
                Month=int(time[i][5]+time[i][6])
                Day=int(time[i][8]+time[i][9])
                Hour=int(time[i][11]+time[i][12])
                Minute=int(time[i][14]+time[i][15])
                Second=int(time[i][17]+time[i][18])
                timestamp.append(pd.Timestamp(year=Year, month=Month, day=Day, hour=Hour, minute=Minute, second=Second))
                time[i]=timestamp[i].strftime("%Y-%m-%d %H:%M:%S")    
        return time

def mean(a):
	average=round((sum(a)/len(a)), 6)
	return average

def cal_speed(u,v):
# wind speed |Vh|= (u**2 + v**2)**(1/2)
	speed =round(math.sqrt(math.pow(u, 2) + math.pow(v, 2)), 6)
	return speed

def cal_dir(u,v):
#meteorological wind direction
	direction=round((math.atan2(-u,-v)*180/math.pi),6)
	return direction

def unit_convert(a): 
#wind speed m/s to knots
	b=[]
	for i in range(len(a)):
		b.append(round(a[i]*1.94384, 6))
	return b

def cal(infile):
#calculate instantanious wind speed and direction
	speed=[]
	direction=[]
	time,u,v=readdata(infile)
	time=time_convert(time)
	for i in range(len(u)):
		speed.append(cal_speed(u[i], v[i]))
		direction.append(cal_dir(u[i], v[i]))
	return time, unit_convert(speed), direction


def cal_avg10(infile):
	time, u,v=readdata(infile)
#calculate 10-minute average wind speed and direction
	time,speed, direction=cal(infile)
	time_avg=[]
	speed_avg=[]
	direction_avg=[]
	for i in range(len(speed)//10): #neglect data if there are less than 10 values left
		speed_avg.append(mean(speed[i*10:(i+1)*10])) ##average wind speed is the average of instantanious speed from 1st to 10th
		time_avg.append(time[i*10] +'-'+ time[(i+1)*10-1])
		direction_avg.append(cal_dir(mean(u[i*10:(i+1)*10]),mean(v[i*10:(i+1)*10]))) #average wind direction is calculated through average u, v
	return time_avg, speed_avg, direction_avg
