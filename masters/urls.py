from django.urls import path, include,re_path
from .views import *

urlpatterns = [
    path('status', StatusView.as_view()),
    path('status/<int:pk>', StatusView.as_view()),
]
