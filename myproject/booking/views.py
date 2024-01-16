from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Concert, Seat

@login_required
def concert_detail(request, name):
    concert = get_object_or_404(Concert, name=name)
    return render(request, 'booking/concert_detail.html', {'concert': concert})

@login_required
def concert_booking_info(request, name):
    concert = get_object_or_404(Concert, name=name)
    user_email = request.user.email
    return render(request, 'booking/concert_booking_info.html', {'concert': concert, 'user_email': user_email})
