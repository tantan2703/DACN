from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
   
    #path('login/', views.Login, name='login'a),
    path('login/', views.LoginUser, name='login'),
    path('login2/', views.login_view, name='login2'),
    path('logout/',views.logoutUser,name = "logout"),
    path('register/',views.register,name = "register"), 
    path('reset_password', auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_send', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
