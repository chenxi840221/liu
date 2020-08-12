import pandas as pd
from readdata import *
from calculate import *
from writedata import *
infile='sample.csv'
outfile_inst='output_inst.csv'
outfile_avg='output_avg10.csv'
case='avg10'
if case=='instantaneous':
	time, speed, direction =cal(infile)
	writedata( outfile_inst, time, speed, direction)
elif case=='avg10':
	time_avg, speed_avg, direction_avg =cal_avg10(infile)
	writedata( outfile_avg, time_avg, speed_avg, direction_avg)

