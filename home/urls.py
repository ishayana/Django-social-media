from django.urls import path
from . import views
from .views import AccessControlMixin


app_name = 'home'
urlpatterns = [
    path('', views.AccessControlMixin.as_view(), name='home'),
    path('blogs', views.BlogView.as_view(), name='blogs'),
    path('blog/<int:blog_id>', views.BlogdetailsView.as_view(), name='blog_details'),
    path('404/', views.PageNotFound.as_view(), name='404'),
]