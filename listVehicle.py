# FINAL SCRIPT - listVehicle.py

from datetime import datetime
import RPi.GPIO as GPIO
import os
import time
import pynmea2
import serial
import json
import can

# CAN initialization
print('Bring up CAN0....')
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
try:
    can_interface = 'can0'
    bus = can.interface.Bus(can_interface, bustype='socketcan', bitrate=500000, app_name='python-can')
except OSError:
    print('Unsuccessful CAN initialization :(')
    exit()

print('CAN initialization Successful!')

lat = None
lng = None
lat_direction = None
lng_direction = None
temp = None
voltage = None
soc = None
date1 = None
timestamp1 = None

# Configuring RPi mode
GPIO.setmode(GPIO.BOARD)

# Enable Serial Communication
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=0.5)

# Acquiring GPS co-ordinates
while True:
    while True:
        flag = 0
        dataout = pynmea2.NMEAStreamReader()
        newdata = port.readline()

        if newdata[0:6] == "$GPGGA":
            newmsg = pynmea2.parse(newdata)
            try:
                lat = newmsg.lat
                lat = float(lat)/100
                lng = newmsg.lon
                lng = float(lng) / 100
            except ValueError:
                print("Unsuccessful co-ordinate conversion")
            lat_direction = newmsg.lat_dir
            lng_direction = newmsg.lon_dir
            print('\nPrinting GPS Data\n')
            print('\nLatitude: ' + str(lat))
            print('\nLongitude: ' + str(lng))
            print('\nLatitude Direction: ' + str(lat_direction))
            print('\nLongitude Direction: ' + str(lng_direction))
            print('\n')
            flag = 1
            break

    # Printing CAN Frame
    try:
        if flag == 1:
            message = bus.recv()  # Wait until a message is received.
            f1 = '{0:f} {1:x} {2:x} '.format(message.timestamp, message.arbitration_id, message.dlc)
            str(message.data)
            data_frame = ''
            for i in range(message.dlc):
                data_frame += '{0:x} '.format(message.data[i])
            print(' {}'.format(f1 + data_frame))
            temp = str(message.data[0])
            voltage = str(message.data[1])
            soc = str(message.data[2])
            date1 = datetime.fromtimestamp(message.timestamp).strftime('%Y-%m-%d')
            timestamp1 = datetime.fromtimestamp(message.timestamp).strftime('%H:%M:%S')
            print('\nPrinting CAN Frame Data\n')
            print('\nTemperature: ' + str(temp))
            print('\nVoltage: ' + str(voltage))
            print('\nSOC: ' + str(soc))
            print('\nDate: ' + str(date1))
            print('\nTime: ' + str(timestamp1))
            print('\n')

    except KeyboardInterrupt:
        # Catch keyboard interrupt
        os.system("sudo /sbin/ip link set can0 down")
        print('\n\rCAN Interrupted')

    # Data to be sent to server
    DataTable = {
        "start": "*",
        "header": "0",
        "vendorID": "0",
        "firmwareVersion": "0",
        "packetType": "0",
        "packetStatus": "0",
        "IMEI": "526088520257759",
        "vehicleDetails": "MH04ED4413",
        "GPSFix": "0",
        "date": str(date1),
        "time": str(timestamp1),
        "latitude": str(lat),
        "latitudeDirection": str(lat_direction),
        "longitude": str(lng),
        "longitudeDirection": str(lng_direction),
        "speed": "0",
        "heading": "0",
        "noOfSat": "0",
        "altitude": "0",
        "PDOP": "0",
        "HDOP": "0",
        "networkOperator": "0",
        "IGNStatus": "0",
        "mainPower": "0",
        "mainInputVoltage": "0",
        "batteryVoltage": str(voltage),
        "emergencyStatus": "0",
        "GSMStrength": "0",
        "MCC": "0",
        "MNC": "0",
        "LAC": "0",
        "cellID": "0",
        "NMR": "0",
        "digitalInputStatus": "0",
        "digitalOutputStatus": "0",
        "frameNumber": "0",
        "checksum": "0",
        "end": "$",
        "soc": str(soc),
        "temp": str(temp)
    }

    DT = json.dumps(DataTable)
    length_DT = len(DT)

    # GPRS Communication Begins
    # Transmitting AT Commands to SIM900A
    # '\r\n' indicates the Enter key
    port.write('AT' + '\r\n')  # Check communication
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print("\nChecking GSM Communication...\n")

    port.write('AT+SAPBR=3,1,\"Contype\",\"GPRS\"' + '\r\n')  # Configure bearer profile
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print("\nConfiguring GPRS Profile\n.")

    port.write('AT+SAPBR=3,1,\"APN\",\"airtelgprs.com\"' + '\r\n')  # APN of Provider
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print("\nAPN of Provider - Airtel\n")

    port.write('AT+SAPBR=1,1' + '\r\n')  # Open GPRS context
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print("\nOpening GPRS Context\n.")

    port.write('AT+SAPBR=2,1' + '\r\n')  # Query the GPRS
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print("\nQuerying the GPRS\n.")

    port.write('AT+HTTPSSL' + '\r\n')  # Enable HTTP service
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print("\nEnabling HTTP...\n")

    port.write('AT+HTTPINIT' + '\r\n')  # Initializes HTTP service
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print("\nHTTP Initialized\n.")

    port.write('AT+HTTPPARA=\"CID\",1' + '\r\n')  # Sets CID parameter for HTTP Session
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print("\nCID Parameters Set\n.")

    port.write('AT+HTTPPARA=\"URL\",\"http://7c378c83a965.ngrok.io/listvehicles/?format=api\"' + '\r\n')  # Server Address
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print("\nNGROK\n")

    port.write('"AT+HTTPPARA=\"CONTENT\",\"application/json\"' + '\r\n')  # Set data type
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)

    port.write('AT+HTTPDATA=' + str(length_DT) + ',100000' + '\r\n')  #
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)

    port.write(DT)  # Sending Data to Server
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print("\nSending Data to server\n")

    port.write('AT+HTTPACTION=1' + '\r\n')  # Start POST session
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print("\nData POSTED\n")

    port.write('AT+HTTPTERM' + '\r\n')  # Terminate HTTP Service
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print('\nTerminating HTTP...\n')

    port.write('AT+SAPBR=0,1' + '\r\n')  # Close GPRS context
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    print('\nSession Ended')