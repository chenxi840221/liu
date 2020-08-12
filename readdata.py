import csv

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

