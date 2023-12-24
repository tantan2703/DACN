from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:     
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
#from .models import Order
class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = '__all__'
		exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
      #  model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']