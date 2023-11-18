from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.signup, name='signup'),
]
