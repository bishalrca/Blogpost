# blog/views.py

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog, Comment
from .forms import BlogForm

class BlogListView(View):
    template_name = 'templates/home.html'

    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'blogs': blogs})

class BlogCreateView(LoginRequiredMixin, View):
    template_name = 'templates/create_blog.html'
    form_class = BlogForm
    success_url = 'home'  

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'create_blog.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog created successfully')
            return redirect(self.success_url)
        return render(request, 'create_blog.html', {'form': form})

class BlogUpdateView(LoginRequiredMixin, View):
    template_name = 'templates/create_blog.html'
    form_class = BlogForm
    success_url = 'home'

    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        form = self.form_class(instance=blog)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog updated successfully')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class BlogDeleteView(LoginRequiredMixin, View):
    success_url = 'home'

    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        blog.delete()
        messages.success(request, 'Blog deleted successfully')
        return redirect(self.success_url)


class BlogDetailView(View):
    template_name = 'tempaltes/blog_detail.html'

    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        return render(request, 'blog_detail.html', {'blog': blog})
