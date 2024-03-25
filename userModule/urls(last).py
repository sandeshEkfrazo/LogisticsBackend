from django.urls import path
from .views import *

urlpatterns = [
    path('total-amount-after-completeion-of-ride', TotalAmountAfterRideComplete.as_view()),
    path('book-user-vehicle', BookVehicleAPI.as_view()),
    path('get-order-detail/<int:order_id>/user_id/<int:user_id>', BookVehicleAPI.as_view()),
    path('cancel-user-order/<int:order_id>', CancelOrderByUser.as_view()),
    path('getuserOrders', CancelOrderByUser.as_view()),
    path('user-feedback', UserFeedBackApi.as_view()),
    path('biiling-request', BillingRequestApi.as_view()),
    path('recipt-details', UserAndDriverrecipt.as_view()),
    path('updated-driver-document-expiry-dates', DriverDocumentExpiryDate.as_view()),
    path('get-sub-user-phone-number/<int:order_id>', getUserPhoneNumber.as_view()),
    path('send-otp-to-sub-user', getUserPhoneNumber.as_view()),
    path('resend-otp', ResendOTP.as_view()),
    path('all-scheduled-orders', AllScheduledOrder.as_view()),
    path('driver-list-with-distance', DriverWithDistanceAPI.as_view()),
    path('get-otp-details', GetOTPDetails.as_view()),
    path('call-b', CallAPI.as_view()),

    path("delete-tasks", DeleteTasks.as_view())
]
