from django.urls import path
<<<<<<< HEAD
from .views import concert_detail, concert_booking_info, momo_payment
=======
from .views import concert_detail, concert_booking_info, payment, concert_list
>>>>>>> 8f110ddfd33ee64f22bc5c9e80c98a78fbcd5cef
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('concert', concert_list, name='concert'),
    path('concert/<str:name>/', concert_detail, name='concert_detail'),
    path('concert/<str:name>/booking/', concert_booking_info, name='concert_booking_info'),
    path('concert/<str:name>/momo_payment/',  momo_payment, name='momo_payment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

