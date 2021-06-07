from django.db import models
from django import forms
class VehicleData(models.Model):
    # id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=50)
    chassisNo = models.CharField(max_length=17)
    IMEI = models.CharField(max_length=15)
    vehicleRegNo = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=30)
    phoneNo = models.IntegerField()

    def __str__(self):
    	return self.vehicleRegNo

class Vehicle(models.Model):
	vehicleDetails = models.ForeignKey(VehicleData, on_delete=models.CASCADE, related_name='+', to_field='vehicleRegNo')
	#AIS140 Frame begins
	start = models.CharField(max_length=1)
	header = models.CharField(max_length=5)
	vendorID = models.CharField(max_length=4)
	firmwareVersion = models.CharField(max_length=6)
	packetType = models.CharField(max_length=2)
	packetStatus = models.CharField(max_length=1)
	IMEI = models.CharField(max_length=15)
	vehicleRegNo = models.CharField(max_length=10)
	GPSFix = models.CharField(max_length=1)
	date = models.DateField()
	time = models.TimeField()
	latitude = models.CharField(max_length=12)
	latitudeDirection = models.CharField(max_length=1)
	longitude = models.CharField(max_length=12)
	longitudeDirection = models.CharField(max_length=1)
	speed = models.CharField(max_length=4)
	heading = models.CharField(max_length=6)
	noOfSat = models.CharField(max_length=2)
	altitude = models.CharField(max_length=6)
	PDOP = models.CharField(max_length=6)
	HDOP = models.CharField(max_length=6)
	networkOperator = models.CharField(max_length=15)
	IGNStatus = models.CharField(max_length=1)
	mainPower = models.CharField(max_length=1)
	mainInputVoltage = models.CharField(max_length=4)
	batteryVoltage = models.CharField(max_length=4)
	emergencyStatus = models.CharField(max_length=1)
	GSMStrength = models.CharField(max_length=2)
	MCC = models.CharField(max_length=3)
	MNC = models.CharField(max_length=4)
	LAC = models.CharField(max_length=4)
	cellID = models.CharField(max_length=6)
	NMR = models.CharField(max_length=10)
	digitalInputStatus = models.CharField(max_length=4)
	digitalOutputStatus = models.CharField(max_length=2)
	frameNumber = models.CharField(max_length=6)
	checksum = models.CharField(max_length=4)
	end = models.CharField(max_length=1)
	#AIS140 Frame ends
	soc = models.CharField(max_length=4)
	temp = models.CharField(max_length=4)

	def __str__(self):
		return self.frameNumber 
    

