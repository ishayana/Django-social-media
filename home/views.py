from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from userprofile.views import UserfeedView


#In this section we mixin two veiws on one URL:
class AccessControlMixin(UserPassesTestMixin, View):
    #TestFunc is used to check whether a user is authenticated or not.
    #NO? handel_no_permission 
    #YES? get 
    def test_func(self):
        return self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return HomeView.as_view()(self.request)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return UserfeedView.as_view()(self.request)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return UserfeedView.as_view()(self.request)
        return self.handle_no_permission()


#Home page for unauthenticated users.
class HomeView(View):
    form_class = RegistrationForm 
    template_name = 'home/home.html'
    def get(self, request):
        form = self.form_class 
        context = {'form' : form}
        if request.user.is_authenticated:
            username = request.user.username
            context['username'] = username
        return render(request, self.template_name , context)

    #This section is about Registration user
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                first_name = cd['firstname'],
                last_name = cd['lastname'],
                username = cd['username'],
                email= cd['email'],
                password= cd['password']
                )
            messages.success(request, 'Your account created successfully!', 'success')
            return redirect('home:home')
        return render(request, self.template_name , { 'form' : form })
    
class PageNotFound(View):
    def get(self, request):
        return render(request, 'errors/404.html')