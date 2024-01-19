from django.urls import path
from .views import concert_detail, concert_booking_info, payment
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('concert/<str:name>/', concert_detail, name='concert_detail'),
    path('concert/<str:name>/booking/', concert_booking_info, name='concert_booking_info'),
    path('concert/<str:name>/payment/', payment, name='payment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

