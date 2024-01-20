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
<<<<<<< HEAD
import json
import uuid
import requests
import hmac
import hashlib

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

=======
from django.core.paginator import Paginator

def concert_list(request):
    concerts=Concert.objects.all()
    paginator = Paginator(concerts,6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context={
        'concerts':paged_listings,
       
    }
    return render(request, "booking/concert.html",context)
>>>>>>> 8f110ddfd33ee64f22bc5c9e80c98a78fbcd5cef

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
@csrf_exempt
def momo_payment(request, name):
    if request.method == 'POST':
        # Lấy thông tin concert từ database
        concert = get_object_or_404(Concert, name=name)

        # Các thông tin cần thiết cho thanh toán MoMo
        partnerCode = "MOMO"
        accessKey = "F8BBA842ECF85"
        secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
        
        # Loại bỏ dấu chấm từ tổng giá vé
        raw_total_price = request.POST.get('total_price', '0.000')
        amount = raw_total_price.replace(".", "")

        orderInfo = f"Pay for concert: {concert.name}"  # Sử dụng tên concert trong orderInfo
        redirectUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
        ipnUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"

        # Các thông tin khác cần thiết
        orderId = str(uuid.uuid4())
        requestId = str(uuid.uuid4())
        requestType = "captureWallet"
        extraData = ""  # pass empty value or Encode base64 JsonString
        # Tạo chữ ký
        rawSignature = (
            f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}"
            f"&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}"
            f"&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"
        )
        h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
        signature = h.hexdigest()

        # Dữ liệu gửi đi
        momo_data = {
            'partnerCode': partnerCode,
            'partnerName': "Test",
            'storeId': "MomoTestStore",
            'requestId': requestId,
            'amount': amount,
            'orderId': orderId,
            'orderInfo': orderInfo,
            'redirectUrl': redirectUrl,
            'ipnUrl': ipnUrl,
            'lang': "vi",
            'extraData': extraData,
            'requestType': requestType,
            'signature': signature
        }

        # In ra JSON request
        print("--------------------JSON REQUEST----------------")
        print(json.dumps(momo_data, indent=4))

        # Gửi HTTP POST request tới endpoint của MoMo
        momo_url = "https://test-payment.momo.vn/v2/gateway/api/create"
        headers = {'CONTENT_TYPE': 'application/json'}
        response = requests.post(momo_url, json=momo_data, headers=headers)

        # Xử lý kết quả và trả về
        result = response.json()
        pay_url = result.get('payUrl', '')

        # In ra JSON response
        print("--------------------JSON RESPONSE----------------")
        print(json.dumps(result, indent=4))

        if pay_url:
            # Chuyển hướng người dùng đến trang thanh toán
            return redirect(pay_url)
        else:
            return JsonResponse({'error': 'PayUrl not found'})


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

        # Tạo đường dẫn tới thư mục media/qr_codes
        qr_codes_dir = getattr(settings, 'QR_CODES_DIR', 'qr_codes')
        qr_codes_path = os.path.join(settings.MEDIA_ROOT, qr_codes_dir)

        # Tạo thư mục nếu nó chưa tồn tại
        if not os.path.exists(qr_codes_path):
            os.makedirs(qr_codes_path)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        payment_info = f"Concert: {concert_name}\nTickets: {total_tickets}\nSeats: {selected_seats}\nTotal Price: ${total_price}"
        qr.add_data(payment_info)
        qr.make(fit=True)

        # Tạo đường dẫn tới tệp QR
        qr_filename = f'{concert_name}_payment_qr.png'
        relative_qr_path = os.path.join(qr_codes_dir, qr_filename)
        absolute_qr_path = os.path.join(qr_codes_path, qr_filename)

        qr.make_image(fill_color="black", back_color="white").save(absolute_qr_path)

        with transaction.atomic():
            payment_instance = Payment.objects.create(
                user=request.user,
                concert=concert,
                total_tickets=total_tickets,
                total_price=total_price,
                qr_file_name=qr_filename,  # Sử dụng tên tệp mà không có đường dẫn thư mục
                user_email=user_email,
                note=note,
            )


            selected_seats_objects = Seat.objects.filter(concert=concert, seat_number__in=selected_seats)
            payment_instance.selected_seats.set(selected_seats_objects)
        relative_qr_path = relative_qr_path.replace('\\', '/')
        context['qr_code_path'] = relative_qr_path
        print("Relative QR Path:", relative_qr_path)
        return render(request, 'booking/payment.html', context)
    else:
        messages.warning(request, 'Invalid request method.')
        return redirect('home')