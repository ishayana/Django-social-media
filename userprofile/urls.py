from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'userprofile'

urlpatterns = [
    path('<str:username>/', views.UserprofileView.as_view(), name='profile'),
    path('<str:username>/bio', views.UserbioView.as_view(), name='userbio'),
    path('<str:username>/post/<int:post_id>', views.PostDetailsView.as_view(), name='post'),
    path('<str:username>/post/<int:post_id>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('<str:username>/post/<int:post_id>/update', views.PostUpdateView.as_view(), name='post_update'),
    path('follow/<str:username>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<str:username>', views.UserUnfollowView.as_view(), name='user_unfollow'),
    path('<str:username>/comment/<int:comment_id>', views.CommentdetailsView.as_view(), name='comment_details'),
    path('<int:post_id>/like', views.PostLikeView.as_view(), name='post_like'),

#     path('<str:username>/comment/<int:comment_id>/delete', views.CommentDeleteView.as_view(), name='comment_delete'),
#     path('<str:username>/comment/<int:commetn_id>/update', views.CommentUpdateView.as_view(), name='comment_update'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
