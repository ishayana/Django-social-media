from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import PostForm, PostUpdateForm, CommentForm, SearchForm
from django.contrib import messages
from .models import PostModel, FollowModel, CommentModel, LikeModel
from django.urls import reverse
import datetime
import os

#UserProfile page
class UserprofileView(LoginRequiredMixin, View):
    form_class = PostForm
    template_name = 'userprofile/profile.html'
    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        self.followers = self.user.following.all()
        self.followings = self.user.follower.all()
        self.posts = self.user.posts.all().order_by('-created')
        self.realtion = FollowModel.objects.filter(follower=request.user, following=self.user).exists()
        return super().setup(self, request, *args, **kwargs)

    def get(self, request, username):
        #first letter of username for show on avatar
        requsername = request.user.username
        postform = self.form_class
        is_owner = False
        if self.user == request.user:
            is_owner = True
        posts = self.posts
        relation = self.realtion
        is_following = False
        if relation:
            is_following = True
        followers = self.followers
        followings = self.followings
        posts_list= []
        for post in posts:
            commetnNum = post.postcomment.filter(is_reply=False).count() or ''
            like_status = post.user_like(request.user)
            posts_list.append((post, commetnNum, like_status))
        

        
        follower_list = []
        for follower in followers:
            isFollowingReqUser = False
            isFollowingReqUser = FollowModel.objects.filter(follower=request.user, following=follower.follower).exists()
            if isFollowingReqUser:
                isFollowingReqUser = True
            follower_list.append((follower.follower, isFollowingReqUser))

        year = datetime.datetime.now().year
        return render(request, self.template_name , {
            'username' : username,
            'requsername' : requsername,
            'postform' : postform,
            'is_owner' : is_owner,
            'posts' : posts,
            'posts_list' : posts_list,
            'is_following' : is_following,
            'followings': followings,
            'followers' : followers,
            'follower_list' : follower_list,
            'year' : year,
            })

#Home page for authenticated users. (UserFeed page)
class UserfeedView(View):
    template_name = 'userprofile/feed.html'
    model = PostModel
    form_class = PostForm
    search_form_class = SearchForm


    def get(self, request):
        following = FollowModel.objects.filter(follower=request.user).values('following')
        friends = FollowModel.objects.filter(follower__in=following, following=request.user)
        
        # posts = PostModel.objects.filter(author__in=following).order_by('-created')
        postform = self.form_class()
        requsername = request.user.username
        posts = self.model.objects.all().order_by('-created')

        # search form 
        if request.GET.get('search'):
            posts = posts.filter(description__contains=request.GET['search'])

        posts_list = []
        for post in posts:
            comments = post.postcomment.filter(is_reply=False).count() or ''
            like_status = post.user_like(request.user)
            posts_list.append((post, comments, like_status))

        return render(request, self.template_name, {
            'friends' : friends,
            'posts' : posts,
            'posts_list' : posts_list,
            'requsername' : requsername,
            'postform' : postform,
            'searchform' : self.search_form_class
            })

    def post(self, request):
        postform = self.form_class(request.POST, request.FILES)
        if postform.is_valid():
            newpost = postform.save(commit=False)
            newpost.author = request.user
            newpost.save()
            messages.success(request, 'Your post uploaded successfully!', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'postform' : postform})

#for show post detail (like, comments, ...)
class PostDetailsView(LoginRequiredMixin, View):
    model = PostModel
    form_class = CommentForm
    template_name = 'userprofile/postdetails.html'
    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(username=kwargs['username'])
        self.post_instance = get_object_or_404(self.model ,pk=kwargs['post_id'], author_id=self.user.id)

        return super().setup(self, request, *args, **kwargs)

    def get(self, request, username, post_id):
        commentform = self.form_class
        requsername = request.user.username
        post = self.post_instance
        comments = post.postcomment.filter(is_reply=False)
        context = {
            'username' : post.author.username,
            'post' : post,
            'requsername' : requsername,
            'comments' : comments,
            'commentform' : commentform,
                }
        return render(request, self.template_name ,context)
    
    def post(self, request, *args, **kwargs):
        commentform = self.form_class(request.POST)
        if commentform.is_valid():
            commentformnew = commentform.save(commit=False)
            commentformnew.author = request.user
            commentformnew.post = self.post_instance
            commentformnew.is_reply = False
            commentformnew.save()
            messages.success(request, 'Your comment posted!', 'succuss')
            return redirect('userprofile:post', username=self.user.username, post_id=self.post_instance.id )
        return render(request, self.template_name, {'commentform' : commentform})

    

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, username, post_id):
        user = get_object_or_404(User, username=username)
        post = get_object_or_404(PostModel, pk=post_id, author_id=user.id)
        if post.author_id == request.user.id:
            post.delete()
            messages.success(request, "Post deleted successfully!", 'success')
        else:
            messages.error(request, "You cann not delet this post!", 'danger')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostForm
    template_name = 'userprofile/update.html'
    def setup(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        self.post_instance = get_object_or_404(PostModel, pk=kwargs['post_id'], author_id=user.pk)
        return super().setup(request, *args, **kwargs)

    def get(self, request, username, post_id):
        requsername = request.user.username
        post = self.post_instance
        if not post.author_id == request.user.id:
            messages.error(request, "You can not edit this post!", 'danger')
            return redirect("home:home")
        author_id = post.author.id
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'formupdate' : form, 'requsername' : requsername, 'author_id' : author_id})
    
    def post(self, request, username, post_id):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post updated successfully!')
            return redirect(reverse('userprofile:profile' ,args=[username]))
        return render(request, self.template_name, {'form' : form})
        
#Follow user
class UserFollowView(LoginRequiredMixin, View):
    model = FollowModel

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request, username):
        user_to_follow = get_object_or_404(User, username=username)
        relation = self.model.objects.filter(follower=request.user, following=user_to_follow)
        if not relation.exists():
            self.model.objects.create(follower=request.user, following=user_to_follow)
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#Unfollow user
class UserUnfollowView(LoginRequiredMixin, View):
    model = FollowModel

    def get(self, request, username):
        user_to_unfollow = get_object_or_404(User, username=username)
        relation = self.model.objects.filter(follower=request.user, following=user_to_unfollow)
        if relation.exists():
            self.model.objects.filter(follower=request.user, following=user_to_unfollow).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class CommentdetailsView(LoginRequiredMixin, View):
    model = CommentModel
    template_name = 'userprofile/commentdetails.html'
    form_class = CommentForm

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        self.comment = self.model.objects.get(author=self.user, pk=kwargs['comment_id'])
        self.commentNum = CommentModel.objects.filter(reply=self.comment).count()
        return super().setup(self, request, *args, **kwargs)

    def get(self, request, username, comment_id):
        commentNum = self.commentNum
        commentform = self.form_class
        requsername = request.user.username
        comment = self.comment
        user = self.user
        context = {
            'comment' : comment,
            'requsername' : requsername,
            'commentform' : commentform,
            'commentNum' : commentNum
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        commentform = self.form_class(request.POST)
        if commentform.is_valid():
            commentformnew = commentform.save(commit=False)
            commentformnew.author = request.user
            commentformnew.is_reply = True
            commentformnew.post = self.comment.post
            commentformnew.reply = self.comment
            commentformnew.save()
            messages.success(request, 'Your comment posted!', 'success')
            return redirect('userprofile:comment_details', username=self.user.username, comment_id=self.comment.id)
        messages.error(request, 'Your comment posted!', 'error')
        return render(request, self.template_name, {'commentform' : commentform})
        
class PostLikeView(LoginRequiredMixin, View):
    model = LikeModel

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        user_id = request.user.id

        user_like = LikeModel.objects.filter(user=user_id, post=post_id)
        if user_like.exists():
            user_like.delete()
        else:
            LikeModel.objects.create(user=request.user, post_id=post_id)
        next_page =request.GET.get('next', '/')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
