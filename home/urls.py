from django.urls import path
from . import views
from .views import AccessControlMixin


app_name = 'home'
urlpatterns = [
    path('', views.AccessControlMixin.as_view(), name='home'),
    path('404/', views.PageNotFound.as_view(), name='404'),
]