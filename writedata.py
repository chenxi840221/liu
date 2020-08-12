import csv
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
