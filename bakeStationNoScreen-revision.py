import time
import datetime

import serial
import csv
import os, glob
import numpy as np

from math import log

def getPressure(physAddress):
    # Connect to the ion gauge hooked up to physAddress and query for pressure
    try:
        ser = serial.Serial(physAddress, 9600, timeout =  10)
        ser.write(b'#0002I1\r')
        ser.flush()
        message = ser.read(11)
        ser.close()
        pressure = float(message[1:-1].decode("utf-8"))
        
        # Safety feature: if pressure is higher than threshold, switch off ion gauge
        if pressure > pressureThreshold:
            ser = serial.Serial(physAddress, 9600, timeout =  10)
            ser.write(b'#0030I1\r')
            ser.flush()
            ser.close()
        
    except:
        pressure = 0.0
        print('There was a problem in the serial communication to the Multi Gauge.')
    return pressure
        
def thermistorFun(resistance, R25):
    # Assuming a specific 100 kOhm thermistor, this returns the temperature
    B = 4092.0
    T0 = 298.0
    temperature = B * T0 / (B - T0 * log(R25 / resistance)) - 273
    return temperature

def getTemperature(physAddress):
    # Connect to the Itsy Bitsy reading in the voltage across the thermistor
    R25 = 100.0E3 # Thermistor value
    Rpullup = 100.0E3
    try:
        ser = serial.Serial(physAddress, timeout = 5)
        ser.write(b'boguscommand\r\n') # It doesn't matter precisely which command we send
        ser.readline()  # Do a dummy because that's how the Itsy Bitsy be
        message = ser.readline()[:-2]
        ser.close()
        value = float(message)/2**16
        resistance = Rpullup * value / (1 - value)
        temperature = thermistorFun(resistance, R25)
    except:
        print('There was a problem in the serial communication to the thermistor. Try unplugging the device.')
        temperature = 0.0
    return temperature

def getThermocoupleTemp(physAddress):
    temperatures = []
    
    try:
        ser = serial.Serial(physAddress, timeout = 5)
        ser.write(b'somecommand\r\n')
        #ser.flush()
        time.sleep(5)
        #print(ser.inWaiting())
        while ser.inWaiting() > 0:
            msg = ser.readline()
            temp = float(msg[:-2])
            #print(temp)
            #temperatures.append(ser.readline())
            temperatures.append(temp)
        ser.close()
    except:
        print('There was a problem in the serial communication to thermocouple(s). Figure it out.')
        temperatures = ['err']
    return temperatures

def readCSVFile(filename):
    # Read in data from file named filename
    dum = []
    with open(filename, 'r') as infile:
        reader = csv.reader(infile, delimiter = ',')
        for row in reader:
            dum.append(row)
        # Strip off header
        dum = dum[1:]
    return dum

def appendToCSVFile(filename, data):
    try:
        with open(filename, 'a', newline = '') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(data)
    except:
        print("Error", "Couldn't write to csv file for some reason")


def addPoint(physAddressIonGauge, physAddressThermo, physAddressTC, filename):
    # Does everything to add a new point and update everything

    pressure = getPressure(physAddressIonGauge)
    temperature = getTemperature(physAddressThermo)
    TC_temperatures = getThermocoupleTemp(physAddressTC)
    #~#~#~#~#~#~#~#~# thermocouple temperatures TC_temperatures is a list and is appended to data

    
    while pressure == 'NaN':
        pressure = getPressure(physAddressIonGauge)
    reltime = int(time.time())
    nowtime = datetime.datetime.now()
    curtime = time.strftime('%H:%M %d %h %Y')


    #~#~#~#~#~#~#~# put data together
    data = [curtime, reltime, pressure, temperature]


    #~#~#~#~#~#~#~# append TC_temperatures
    for i in range(len(TC_temperatures)):
                data.append(TC_temperatures[i])

    # Add to file
    appendToCSVFile(filename, data)
    print(data)

if __name__ == "__main__":
    # Some configuration parameters, may be set via GUI later
    physAddressIonGauge = '/dev/ttyUSB0'
    physAddressThermo = '/dev/ttyACM0'
    physAddressTC = '/dev/ttyACM1'
    #~#~#~#~#~#~#~#~ Update physAdressTC from adress in raspberry pi

    samplePeriod = 10   # In seconds
    pressureThreshold = 1.0E-5  # Threshold above which we should switch off the ion gauge
    
    # Create directories for data and figures if they don't exist yet
    if not os.path.exists('logdata'):
        os.makedirs('logdata')
        
    # Continue using previous savefile?
    inp = input("Coninue using previous savefile? [y/n]")
    if inp == 'y':
        try:
            # Get most recent file
            allfiles = glob.glob("logdata/*.csv")
            #print(allfiles)
            allfiles.sort(reverse = True)
            #print(allfiles)
            filename=allfiles[0]
            print(filename)
        except:
            print("Couldn't open previous file. Starting afresh.")
            # Create new file based on time specification
            filename = 'logdata/' + time.strftime('%Y%m%d_%H%M') + '.csv'
    else:
        # Create new file based on time specification
        print("Creating new file.")
        filename = 'logdata/' + time.strftime('%Y%m%d_%H%M') + '.csv'
    
    try:
        while True:
            addPoint(physAddressIonGauge, physAddressThermo, physAddressTC, filename)
            #~#~#~#~#~#~#~#~# now addPoint takes the physical Address for the thermocouples physAddressTC
            
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopping.")
