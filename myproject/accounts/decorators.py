from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("You are already logged in.")
            # Hoặc bạn có thể chuyển hướng đến một trang khác
            # return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func