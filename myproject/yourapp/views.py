from django.shortcuts import render

def example_view(request):
    return render(request, 'Musical/single_blog.html')