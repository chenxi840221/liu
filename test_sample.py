import csv
import math
import pandas as pd
import random

def readdata(file):
#read file and get variables time,u,v
    time=[]
    u=[]
    v=[]
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0 
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} U(m/s) {row[1]}, v(m/s) {row[2]}.')
                time.append(row[0])
                u.append(float(row[1])) 
                v.append(float(row[2]))
                line_count += 1
        print(f'Processed {line_count} lines.')
    return time, u, v

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

def writedata(fileout, time, speed, direction):
        csv = open(fileout, "w")
        #"w" indicates that you're writing strings to the file
        columnTitleRow = "datetime, WindSpeed(knots), WindDir\n"
        csv.write(columnTitleRow)
        for i in range(len(time)):
            row=str(time[i])+","+str(speed[i])+","+str(direction[i])+"\n"
            print(row)
            csv.write(row)
        csv.close()

####test####

def test_answer():
	infile = './test_sample.csv'
        #test csv file reading
	time, u, v =readdata(infile)
	assert time[9] == '2020-03-27 04.09.00'
	assert u[9] == 1.753224
	assert v[9] == -3.335626

	u_test=random.randrange(-30, 30, 0.01)
	v_test=random.randrange(-30, 30, 0.01)
	#test cal_speed
	assert cal_speed(u_test, v_test) >= math.abs(u_test) and cal_speed(u_test, v_test) >= math.abs(v_test) and cal_speed(u_test, v_test) <= math.abs(u_test) + math.abs(v_test)
	# test cal_dir
	if u_test >= 0 and v_test >=0:
		assert cal_dir(u_test,v_test) >= -180 and cal_dir(u_test,v_test) <= -90
	elif u_test >= 0 and v_test <=0:
		assert cal_dir(u_test,v_test) >= -90 and cal_dir(u_test,v_test) <= -0
	elif u_test <= 0 and v_test >=0:
		assert cal_dir(u_test,v_test) >= 90 and cal_dir(u_test,v_test) <= 180
	elif u_test <= 0 and v_test <=0:
		assert cal_dir(u_test,v_test) >= 0 and cal_dir(u_test,v_test) <= 90
		 
	#test cal()
	time_converted, speed, direction= cal(infile)
	assert time_converted[9] == '2020-03-27 04:09:00'
	i=random.randrange(1, len(time), 1)
	assert speed[i]== math.sqrt(math.pow(u[i], 2) + math.pow(v[i], 2))
	assert direction[i]== cal_dir(u[i], v[i])
	
	#test cal_avg10()
	time_avg, speed_avg, direction_avg= cal_avg10(infile)
	assert time_avg[1]=='2020-03-27 04:10:00-2020-03-27 04:19:00'
	assert speed_avg[1] >= min(speed[0:10]) and speed_avg[1] <= max(speed[0:10])
	assert direction_avg[1] >= min(direction[0:10]) and direction_avg[1] <= max(direction[0:10])

	#test writedata
	assert str(time[1])+","+str(speed[1])+","+str(direction[1]) =='2020-03-27 04:01:00,8.174601,-23.993329'


 #   assert direction(['2020-03-27 04.05.00','1.662758','-3.345694']) == -153.5733366
