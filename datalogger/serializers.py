from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vehicle
		fields = ('start', 'header', 'vendorID', 'firmwareVersion', 'packetType', 'packetStatus', 'IMEI', 'vehicleDetails', 'GPSFix', 'date', 'time', 'latitude', 'latitudeDirection', 'longitude', 'longitudeDirection', 'speed', 'heading', 'noOfSat', 'altitude', 'PDOP', 'HDOP', 'networkOperator', 'IGNStatus', 'mainPower', 'mainInputVoltage', 'batteryVoltage', 'emergencyStatus', 'GSMStrength', 'MCC', 'MNC', 'LAC', 'cellID', 'NMR', 'digitalInputStatus', 'digitalOutputStatus', 'frameNumber', 'checksum', 'end' ,'soc', 'temp')
