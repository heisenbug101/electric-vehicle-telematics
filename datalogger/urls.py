from django.urls import include, path
from rest_framework import routers
from .import views
from .views import home, dataLogger, vehicleRegistration

router = routers.DefaultRouter()
router.register(r'vehicles', views.VehicleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	path('list', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	path('', home),
	path('datalogger/',dataLogger),
	path('register/',vehicleRegistration),
]
