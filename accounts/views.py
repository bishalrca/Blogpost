from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from blog.models import Blog
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import logout
from django.contrib import messages

User = get_user_model()

#use this to show context
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.all().order_by('-created_at')[:1]
        return context

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
        blogs = Blog.objects.all().order_by('-created_at')[:1]
        return render(request, self.template_name, {'form': form, 'blogs': blogs})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        blogs = Blog.objects.all().order_by('-created_at')[:1]
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form, 'blogs': blogs})
        

class ProfileView(View):
    template_name = 'registration/profile.html'

    def get(self, request, *args,**kwargs):
        blogs = Blog.objects.all().order_by()[:1]
        profile = get_object_or_404(CustomUser, id=kwargs['pk'])
        return render(request, self.template_name,{'profile':profile, 'blogs':blogs})
    
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