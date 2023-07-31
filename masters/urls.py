from django.urls import path, include,re_path
from .views import *

urlpatterns = [
    path('status', StatusView.as_view()),
    path('status/<int:pk>', StatusView.as_view()),

    path('filesize/', FilesizeApi.as_view()),
    path('filesize/<int:pk>', FilesizeApi.as_view()),

    path('queries/', QueriesApi.as_view()),
    path('queries/<int:pk>', QueriesApi.as_view()),

    path('language/', LanguageApi.as_view()),
    path('language/<int:pk>', LanguageApi.as_view()),

    path('subscription/', SubscriptionplanApi.as_view()),
    path('subscription/<int:pk>', SubscriptionplanApi.as_view()),

    path('Aboutus/', AboutusApi.as_view()),
    path('Aboutus/<int:pk>', AboutusApi.as_view()),

    path('book-distance/',BookingDistanceApiView.as_view(),name= "for getting all the datas"),
    path('booking_distances/<int:pk>/', BookingDistanceApiView.as_view(), name='booking_distance_detail'),

    path('time/',CustomizavleTimeSearchApiView.as_view(),name= "for getting all the datas"),
    path('time/<int:pk>/', CustomizavleTimeSearchApiView.as_view(), name='time details ')


]
