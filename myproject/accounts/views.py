from django.shortcuts import render, redirect,  HttpResponseRedirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User, auth
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .decorators import *

from bootstrap_modal_forms.generic import BSModalLoginView,BSModalCreateView
from .forms import CustomAuthenticationForm
from .forms import CustomUserCreationForm

class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = '/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('home')
#  Create your views here.

def Login(request):
    if request.user.is_authenticated: 
        pass
    else: 
        messages.info(request,"Please Login to access this pages!")
        return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Điều hướng đến trang chủ hoặc trang khác
        else:
            error_message = 'Invalid username or password.'
    else:
        error_message = ''
    return render(request, 'accounts/login.html', {'error_message': error_message})

@unauthenticated_user
def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = ''
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            # Check username
            if User.objects.filter(username = username).exists():
                messages.error(request,username + ' ' +' already exists. Please try another username')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                if User.objects.filter(email = email).exists():
                    messages.error(request,'Email ' + ' ' + email +' ' +' already being used. Please try another email')
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    user = User.objects.create_user(username = username,
                    password = password1,email=email,first_name = first_name,
                    last_name = last_name)
                    user.save()
                    
                    messages.success(request,  'Account was created for ' + ' ' + username+'. Please login !')
                    return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request,'Password and confirm password does not match')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def LoginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #return HttpResponseRedirect('/')
            #HttpResponseRedirect(request.path_info)
        else: 
            messages.error(request, 'Username or Password is Incorrect')
            
    context ={
        
    }
    return redirect(request.META.get('HTTP_REFERER'))
    #return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'modal/login1.html'
    success_message = 'Success: You were successfully logged in.'
    extra_context = dict(success_url=reverse_lazy('home'))

@ login_required
def favourite_list(request):
    user=request.user
    favourites=user.favourite.all()
    context= {
        'favourites':favourites,
    }
    return render(request,'accounts/favourites.html',context)


def favourite_add(request, pk):
    post = get_object_or_404(Listing, id=pk)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


'''
def dashboard(request):
    user_contacts = Contact.objects.filter(user_id = request.user.id).order_by('-contact_date')
    context = {
        'contacts': user_contacts,
    }
   return render(request,'accounts/dashboard.html',context)
'''
class PasswordsChangeView(PasswordChangeView):
    form_class=PasswordChangeForm
    success_url: reverse_lazy('home')
     
@login_required(login_url='login' )
def changepwd(request):
    if request.method == 'POST':
        user= request.user
        password = request.POST.get('password')
        password1 = request.POST.get('password')
        if password == password1:
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request,'Password and confirm password does not match')
            #return redirect('changepwd')
    context={
                
    }
    return render(request,'accounts/changepwd.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            messages.info(request, 'Username or Password is Incorrect')
            return render(request,"accounts/login.html")
    context ={
        
    }
    return render(request,'home/index2.html',context)
  
def logoutUser(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))



@login_required(login_url='login' )
def profile(request):
    Profile = request.user.Profile
    form = ProfileForm(instance=Profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES,instance=Profile)
        if form.is_valid():
            form.save()
            #return redirect('/listings')
    context = {
        'form':form
    }
    return render(request,'accounts/profile.html',context)

#@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def profile_setting(request):
    Profile = request.user.Profile
    form = ProfileForm(instance=Profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES,instance=Profile)
        if form.is_valid():
            form.save()
            #return redirect('/listings')
    context = {
        'form':form
    }
    return render(request,'accounts/profile_setting.html',context)



