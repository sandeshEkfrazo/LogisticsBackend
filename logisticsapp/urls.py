from django.urls import path, include,re_path
from . import views
# from . import f_views
from rest_framework import routers
from django.conf.urls.static import static
# from django.conf.urls import url
from logisticsapp.views import *
from .views import *


app_name = 'logisticsapp'

urlpatterns = [
#!------------------    ACCOUNT TABLE    ------------------#!

    path("custom-tempate", templateView),

    path('register', RegistrationApiVew.as_view()),
    path('login', LoginView.as_view()),
    path('forgot-password-send-otp', ForgotPasswordSendOtp.as_view()),
    path('otp-verify-forgot-pass', OtpVerificationForgotpass.as_view()),
    path('password-reset', ForgotPasswordReset.as_view()),
    path('change-password', ChangePassword.as_view()),

    path('signup-phone-number', SignUpPhoneNumberApiView.as_view()),

    path('login-view', LoginApiView.as_view()),

    path('verify-otp', VerifyOtpPhoneNumberApiView.as_view()),

    path('signup-user', SignupUserApiView.as_view()),

    path('signup-driver-owner', SignUpforDriverOrOwner.as_view()),

#!------------------    MASTER TABLE    ------------------#!

    path('user-role-ref', UserRoleRefView.as_view()),
    path('user-role-ref/<int:pk>', UserRoleRefView.as_view()),

    path('vehicle-types', VehicleTypesView.as_view()),
    path('vehicle-types/<int:pk>', VehicleTypesView.as_view()),

    path('city', CityView.as_view()),
    path('city/<int:pk>', CityView.as_view()),

    path('coupons', CouponsView.as_view()),
    path('coupons/<int:pk>', CouponsView.as_view()),

    
    path('subcription-plan', SubscriptionView.as_view()),
    path('subcription-plan/<int:pk>', SubscriptionView.as_view()),

#!------------------------------------------------------------------------------------------


    path('custom-user', CustomUserView.as_view()),  #!   pending
    path('custom-user/<int:pk>', CustomUserView.as_view()),

    path('owner', UserRoleRefView.as_view()),
    path('owner/<int:pk>', UserRoleRefView.as_view()),

    path('driver', DriverView.as_view()),   #!   pending
    path('driver/<int:pk>', DriverView.as_view()),

    path('review', ReviewApiView.as_view()),
    path('review/<int:pk>', ReviewApiView.as_view()),

    path('vehicle/', VehicleView.as_view()),
    path('vehicle/<int:pk>', VehicleView.as_view()),

    path('customer-address', CustomerAddressView.as_view()),
    path('customer-address/<int:pk>', CustomerAddressView.as_view()),


    path('pickup-details', PickupDetailsView.as_view()),
    path('pickup-details/<int:pk>', PickupDetailsView.as_view()),

    path('drop-details', DropDetailsView.as_view()),
    path('drop-details/<int:pk>', DropDetailsView.as_view()),

    path('placed-order', PlacedOrderView.as_view()),
    path('placed-order/<int:pk>', PlacedOrderView.as_view()),

    path('in-order', InOrderView.as_view()),
    path('in-order/<int:pk>', InOrderView.as_view()),


    path('payment-detail', PaymentDetailView.as_view()),
    path('payment-detail/<int:pk>', PaymentDetailView.as_view()),

    path('account-detail', AccountView.as_view()),
    path('account-detail/<int:pk>', AccountView.as_view()),

    path('latitude_longitude', DriverLatitudeLongitudeView.as_view()),

    path('user_destination', UserDestinationsView.as_view()),
    path('sign-up/', UserLoginView.as_view()),
    path('VerifyOtp/', OtpVerificationApi.as_view()),

    path('BookingVehicle/', BookingVehicleApi.as_view()),
    path('CancellationVehicle/', CancellationApi.as_view()),
    path('getOrderDetails/', OrderDeatilAPI.as_view()),
    path('getOrderDetails/<int:pk>', OrderDeatilAPI.as_view()),
    path('user_feedback/', User_feedback.as_view()),
    path('UserSignup/',UserSignup.as_view()),
    path('UserSignup/<int:pk>',UserSignup.as_view()),
    # path('profile_image/<int:pk>', views.profile_image, name='profile_image'),

    path('DriverSignup/',DriverSignup.as_view()),
    path('DriverSignup/<int:user_id>',DriverSignup.as_view()),
    path('updateDriverDetails/<int:driver_id>',DriverSignup.as_view()),
    path('driver', DriverSignup.as_view()),
    path('user-login/', LoginApi.as_view()),
    path('customised_message/', Customised_messageApi.as_view()),
    path('customised_message/<int:pk>', Customised_messageApi.as_view()),
    path('accept_or_decline/<int:pk>', accept_or_declineApi.as_view()),
    path('order_dashboard/', Order_dashboardApi.as_view()),
    path('drivers_status_count/', DriverCountStatusApi.as_view()),
    path('scheduled_orders_count/', ScheduledOrder_countApi.as_view()),

    # path('offline_driver/', Driver_OfflineApi.as_view()),
    # path('driver_queries/', DriverQueriesApi.as_view()),
    # path('driver_queries/<int:pk>', DriverQueriesApi.as_view()), 
    path('filter_order/', Filter_OrdersApi.as_view()),   
    path('Vehicle_estimation_cost/',vehicle_estimation_costApi.as_view()),
    path('driverdocumentstatus/', DriverDocumentStatusApi.as_view()),   
    path('driverdocumentstatus/<int:pk>', DriverDocumentStatusApi.as_view()),
    path('accept_status/', accept_statusApi.as_view()),
    path('remarks/', RemarksApi.as_view()), 
    path('remarks/<int:pk>', RemarksApi.as_view()),
    path('filtercount/', FilterCountApi.as_view()),
    path('documentexpiryvalidity/', DriverDocumentExpiryvalidityApi.as_view()),  
    path('documentexpiryvalidity/<int:pk>', DriverDocumentExpiryvalidityApi.as_view()),
    path('deletesubimage/<int:vehicle_type_id>/', Delete_vehicle_imageApi.as_view()),  
    path('delineorderstatus/', Decline_statusApi.as_view()),
    path('pendingorderstatus/', Pending_statusApi.as_view()),
    path('dateorderdetails/', dateOrderDetailsApi.as_view()),
    path('sendmessage/', SendmessageApi.as_view()),
    path('sendmessage/<int:pk>', SendmessageApi.as_view()),
    path('defaultmessage/', DefaultmessageApi.as_view()),
    path('defaultmessage/<int:pk>', DefaultmessageApi.as_view()),
    path('driveryear/', DriveryearApi.as_view()),
    path('getdrivermsg/', getdrivermsgApi.as_view()),
    path('custommesage/', MessageCustomised.as_view()),
    path('custommesage/<int:pk>', MessageCustomised.as_view()),
    path('vehicle_subscription/', VehicleSubscriptionApi.as_view()),
    # path('vehicle_subscription/<int:vehicle_id>', VehicleSubscriptionApi.as_view()),
    # path('vehiclestatus/', VehiclestatusAPI.as_view()),
    path('schedulehour/', SchedulehourApi.as_view()),
    path('schedulehour/<int:pk>', SchedulehourApi.as_view()),
    path('get_useractive_status/', GetuseractiveStatus.as_view()),
    path('history_of_subscriptionplan/', History_of_SubscriptionplanApi.as_view()),
    path('ride_type/', RidetypeAPI.as_view()),
    path('ride_type/<int:pk>', RidetypeAPI.as_view()),
    path('selected_ride_type/', SelectedRideTypeAPI.as_view()),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
