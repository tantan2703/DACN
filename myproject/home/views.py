from django.shortcuts import render


# Create your views here.

def home(request):
    context={
    }
    return render(request,'home/index.html',context)

def test(request):
    context={
    }
    return render(request,'Musical/index.html',context)