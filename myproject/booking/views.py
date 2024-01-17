from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Concert, Seat
from django.http import HttpResponse
import json

@login_required
def concert_detail(request, name):
    concert = get_object_or_404(Concert, name=name)
    return render(request, 'booking/concert_detail.html', {'concert': concert})

@login_required
def concert_booking_info(request, name):
    concert = get_object_or_404(Concert, name=name)
    user_email = request.user.email

    # Lấy danh sách ghế đã chọn từ query parameters
    selected_seats_str = request.GET.get('seats', '[]')
    selected_seats = json.loads(selected_seats_str)

    # Tính tổng số ghế
    total_seats = len(selected_seats)

    # Lấy tổng giá vé từ query parameters
    total_ticket_price = request.GET.get('total_price', '0.00')

    return render(request, 'booking/concert_booking_info.html', {
        'concert': concert,
        'user_email': user_email,
        'selected_seats': selected_seats,
        'total_seats': total_seats,
        'total_ticket_price': total_ticket_price,
    })

