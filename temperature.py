import os
import glob
import time
import requests
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
	
while True:
        temp_values={}
	temp_values=read_temp()
        # Update the temperature values into the stream
       	req = requests.get(
				"http://data.sparkfun.com/input/zDgzovXQ8xSN22r7GyKp?private_key=Yy1Dxdz7kXTvNNkY594K&"+
				"tempc="+str(temp_values[0])+
				"&tempf="+str(temp_values[1]))
        if req.status_code != 200:
           print "Stream Update Failed"        	
	print "Temeperature Values",temp_values[0],temp_values[1]
        print "Stream Update status",req.text
	time.sleep(10)
