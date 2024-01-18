from django.urls import path
from .views import concert_detail
from .views import concert_booking_info

urlpatterns = [
    path('concert/<str:name>/', concert_detail, name='concert_detail'),
    path('concert/<str:name>/booking/', concert_booking_info, name='concert_booking_info'),
]

