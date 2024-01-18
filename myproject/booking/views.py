import os
import json
import qrcode
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Concert, Seat, Payment

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

    print("Selected Seats in concert_booking_info:", selected_seats)

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

@login_required
def payment(request, name):
    if request.method == 'POST':
        concert = get_object_or_404(Concert, name=name)

        concert_name = request.POST.get('concert_name', '')
        total_tickets = int(request.POST.get('total_seats', 0))
        selected_seats_str = request.POST.get('selected_seats', '[]')
        selected_seats_list = selected_seats_str.split(',')

        try:
            selected_seats = json.loads(json.dumps(selected_seats_list))
        except json.JSONDecodeError as e:
            selected_seats = []
            print("Error decoding selected_seats:", e)

        total_price = request.POST.get('total_price', '0.000')
        phone = request.POST.get('phone', '')
        user_email = request.POST.get('user_email', '')
        note = request.POST.get('note', '')

        context = {
            'concert_name': concert_name,
            'total_tickets': total_tickets,
            'selected_seats': selected_seats,
            'total_price': total_price,
            'phone': phone,
        }

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        payment_info = f"Concert: {concert_name}\nTickets: {total_tickets}\nSeats: {selected_seats}\nTotal Price: ${total_price}"
        qr.add_data(payment_info)
        qr.make(fit=True)

        qr_codes_dir = getattr(settings, 'QR_CODES_DIR', 'qr_codes')
        qr_codes_path = os.path.join(settings.MEDIA_ROOT, qr_codes_dir)

        if not os.path.exists(qr_codes_path):
            os.makedirs(qr_codes_path)

        qr_path = os.path.join(qr_codes_path, f'{concert_name}_payment_qr.png')

        print("QR Path:", qr_path)

        qr.make_image(fill_color="black", back_color="white").save(qr_path)

        with transaction.atomic():
            payment_instance = Payment.objects.create(
                user=request.user,
                concert=concert,
                total_tickets=total_tickets,
                total_price=total_price,
                qr_code_path=qr_path,
                user_email=user_email,
                note=note,
            )

            selected_seats_objects = Seat.objects.filter(concert=concert, seat_number__in=selected_seats)
            payment_instance.selected_seats.set(selected_seats_objects)

        context['qr_code_path'] = qr_path

        return render(request, 'booking/payment.html', context)
    else:
        messages.warning(request, 'Invalid request method.')
        return redirect('home')