import django_filters
from django_filters import DateFilter, DateFromToRangeFilter
from . models import *

class VehicleFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date", lookup_expr="gte", input_formats=['%d-%m-%Y'])
    end_date = DateFilter(field_name="date", lookup_expr="lte", input_formats=['%d-%m-%Y'])
    class Meta:
        model = Vehicle
        fields = ['vehicleDetails', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(VehicleFilter, self).__init__(*args, **kwargs)
        self.filters['vehicleDetails'].label = "Vehicle Registration Number"
        self.filters['start_date'].label = "From (ddmmyyyy)"
        self.filters['end_date'].label = "To (ddmmyyyy)"