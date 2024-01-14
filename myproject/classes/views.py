from django.shortcuts import render


# Create your views here.

def classes(request):
    context={
    }
    return render(request,'Musical/classes.html',context)