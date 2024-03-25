from django.urls import path
from . import views
from .forms import UserPasswordResetForm


app_name = 'accounts' #Same namespase in base url.py 

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('reset/', views.UserPasswordRestView.as_view(form_class = UserPasswordResetForm), name='reset_password'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordConfirmView.as_view(), name='password_confirm'),
    path('reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete')
]