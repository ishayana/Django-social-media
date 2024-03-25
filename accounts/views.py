
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from .forms import LoginForm, UserPasswordResetForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string

class LoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    
    #In this section, we'll prevent unauthenticated users from accessing the feed page!
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, { 'form' : form })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You has been successfully logged in.', 'success')

                #In this section, I try to take the username from the request and send that to the URL as a slug!
                return redirect('home:home')
            messages.warning(request, 'Username or password is incorect!', 'warning')
        return render(request, self.template_name, { 'form' : form })

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully!')
        return redirect('home:home')
    
class UserPasswordRestView(auth_views.PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'
    

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
    

class UserPasswordConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'