from django.urls import path
from .views import concert_detail

urlpatterns = [
    path('concert/<str:name>/', concert_detail, name='concert_detail'),
]

