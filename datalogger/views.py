from django.shortcuts import render
from django.contrib import messages
from rest_framework import viewsets
from .serializers import VehicleSerializer
from .models import Vehicle, VehicleData
from .filters import VehicleFilter


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


def home(request):
    #vehicleItems = Vehicle.objects.all() #order by date and time - last added data (additional field order by datetime.now())
    #vehicleItems = Vehicle.objects.all().raw('SELECT * FROM datalogger_vehicle GROUP BY IMEI WHERE date = (SELECT MAX)')
    #SELECT *
    vehicleItems = Vehicle.objects.all().raw('SELECT * FROM datalogger_vehicle v1 INNER JOIN (SELECT vehicleDetails_id, max(date) as MaxDate, max(time) as MaxTime FROM datalogger_vehicle GROUP BY vehicleDetails_id) v2 ON v1.vehicleDetails_id = v2.vehicleDetails_id AND v1.date = v2.MaxDate AND v1.time= v2.MaxTime')
    #vehicleItems = Vehicle.objects.order_by().order_by('vehicleDetails', '-date','-time').distinct()
    print(vehicleItems)
    return render(request, "home.html", {"vehicleItems": vehicleItems})


def dataLogger(request):
    vehicleItems = Vehicle.objects.all()
    vehicleFilter = VehicleFilter(request.GET, queryset=vehicleItems)
    vehicleItems = vehicleFilter.qs
    #return render(request, "Default.htm")
    return render(request, "datalogger.html", {'vehicleItems':vehicleItems, 'vehicleFilter':vehicleFilter})

def vehicleRegistration(request):
    if request.method == "POST":
        email = request.POST["email"]
        chassisNo = request.POST["chassisNo"]
        IMEI = request.POST["IMEI"]
        vehicleRegNo = request.POST["vehicleRegNo"]
        model = request.POST["model"]
        phoneNo = request.POST["phoneNo"]

        model_object = VehicleData(
            email=email,
            chassisNo=chassisNo,
            IMEI=IMEI,
            vehicleRegNo=vehicleRegNo,
            model=model,
            phoneNo=phoneNo,
        )

        if (
            email == ""
            or chassisNo == ""
            or IMEI == ""
            or vehicleRegNo == ""
            or model == ""
            or phoneNo == ""
        ):
            messages.error(request, "All fields are compulsory.")
        elif len(phoneNo) > 10 or len(phoneNo) < 10:
            messages.error(request, "Please enter a 10 digit mobile number.")
        elif len(vehicleRegNo) < 9 or len(vehicleRegNo) > 10:
            messages.error(request, "Please enter a valid vehicle registration number.")
        else:
            messages.success(request, "Registration Successful.")
            model_object.save()
            # return redirect("#")
    return render(request, "vehicleRegistration.html")
