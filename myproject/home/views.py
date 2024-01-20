from django.shortcuts import render
from booking.models import Concert
from blog.models import Post
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    context={
    }
    return render(request,'home/index.html',context)

def test(request):
    context={
    }
    return render(request,'Musical/index.html',context)
def about(request):
    context={
    }
    return render(request,'home/about.html',context)

def search(request):
    queryset_list = Post.objects.all()


    # Keywords 
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(title__icontains=keywords) |  queryset_list.filter(description__icontains=keywords) 

    #Page
    paginator = Paginator(queryset_list,20)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)        

    context =  {
        
        "listings":paged_listings,
        "values":request.GET,
    }
    return render(request,'home/search.html',context)