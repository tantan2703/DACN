from django.urls import path
from .views import momo_payment, thanks

urlpatterns = [
    # path('example/', example_view, name='example_view'),
    path('momo_payment/', momo_payment, name='payUrl'),
    path('thanks/', thanks, name='thanks'),
]