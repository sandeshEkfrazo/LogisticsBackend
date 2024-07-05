from django.urls import path
from .views import *

urlpatterns = [

    path('driver-order-detail', DriverAPI.as_view()),
    path('drivers-order-detail', DriverOrderAPI.as_view()),
    path('update-driver-online-status/', UpdateDriveOnlineApi.as_view()),
    path('update-driver-location', updateDriverLocation.as_view()),
    path('driver-overall-ratings/', DriverEarningsAndratingAPI.as_view()),
    path('driver-overall-ratings/<int:pk>', DriverEarningsAndratingAPI.as_view()),
    path("notify-driver-document-expiry", NotifyDriverDocumentExpiry.as_view()),
    path("drivertotal_earning/", DriverEarningReport.as_view()),
    path('assign-vehicle-to-new-driver', AssignVehicleToDriver.as_view()),
    path('drivers-ride-history', DriverRideHistoryAPI.as_view()),
    path('calculate-eta/', CalculateETA.as_view(), name='calculate_eta'),
]