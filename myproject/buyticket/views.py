from email import message
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.

def buyticket(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        show = request.POST.get('show')
        count = request.POST.get('count')
        seat = request.POST.get('seat')
        note = request.POST.get('note')

        data = {
            'name': name,
            'email': email,
            'phone': phone,
            'show': show,
            'count': count,
            'seat': seat,
            'note': note,
        }
        message_body = '''
        Tên: {}
        Email: {}
        Điện thoại: {}
        Show: {}
        Số lượng vé: {}
        Ghế đã đặt: {}
        Ghi chú: {}
        '''.format(data['name'], data['email'],data['phone'], data['show'],data['count'], data['seat'], data['note'])
        send_mail('Thông tin đặt vé', message_body, '', ['20520378@gm.uit.edu.vn'])
        return HttpResponse('Chúc mừng bạn đã đặt vé thành công - Thông tin vé sẽ được gửi qua email')
    return render(request,'Musical/contact.html', {})