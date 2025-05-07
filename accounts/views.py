from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import logout
from django.contrib import messages

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return '/'
    
class CustomLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('accounts:login')
    



class SignupView(View):
    template_name = 'registration/signup.html'

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})
        

class ProfileView(View):
    template_name = 'registration/profile.html'

    def get(self, request, *args,**kwargs):
        profile = get_object_or_404(CustomUser, id=kwargs['pk'])
        return render(request, self.template_name,{'profile':profile})
    
class ProfileEditView(View):
    template_name = 'registration/profile_edit.html'   

    def get(self,request, *args, **kwargs):
        customuser = get_object_or_404(CustomUser, id=kwargs['pk'])
        form = ProfileUpdateForm(instance = customuser)

        return render (request, self.template_name, {'form': form, 'customuser': customuser})

    def post(self, request, *args, **kwargs):
        customuser = get_object_or_404(CustomUser, id=kwargs['pk'])
        form = ProfileUpdateForm(request.POST,request.FILES,instance = customuser)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile', pk=customuser.pk)

        return render (request, self.template_name, {'form': form, 'customuser': customuser})

    
class LogoutView(View):
    template_name = 'registration/logout.html'

    def get(self,request,*args,**kwargs):
        print("hello world is fucked ")
        return render(request, self.template_name)

    def post(self,request,*args, **kwargs):
           logout(request)
           return redirect('accounts:home')