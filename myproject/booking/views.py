from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Concert, Seat

@login_required
def concert_detail(request, name):
    concert = get_object_or_404(Concert, name=name)
    seats = Seat.objects.filter(concert=concert)
    return render(request, 'booking/index.html', {'concert': concert, 'seats': seats})
