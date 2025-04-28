# blog/views.py

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog, Comment
from .forms import BlogForm

# Blog List View
class BlogListView(View):
    template_name = 'blog/home.html'

    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.all().order_by('-created_at')
        return render(request, self.template_name, {'blogs': blogs})

# Blog Create View
class BlogCreateView(LoginRequiredMixin, View):
    template_name = 'blog/create_blog.html'
    form_class = BlogForm
    success_url = 'home'  # name of your URL pattern

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog created successfully')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

# Blog Update View
class BlogUpdateView(LoginRequiredMixin, View):
    template_name = 'blog/create_blog.html'
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

# Blog Delete View
class BlogDeleteView(LoginRequiredMixin, View):
    success_url = 'home'

    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        blog.delete()
        messages.success(request, 'Blog deleted successfully')
        return redirect(self.success_url)

# Blog Detail View
class BlogDetailView(View):
    template_name = 'blog/blog_detail.html'

    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        return render(request, self.template_name, {'blog': blog})
