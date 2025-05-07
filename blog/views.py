# blog/views.py

from django.views import View
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog, Comment
from .forms import BlogForm, CommentForm

class BlogListView(View):
    template_name = 'templates/home.html'

    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'blogs': blogs})

class BlogCreateView(LoginRequiredMixin, View):
    template_name = 'templates/create_blog.html'
    form_class = BlogForm
    success_url = 'blog:home'  

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        blogs = Blog.objects.all().order_by('-created_at')[:1]
        return render(request, 'create_blog.html', {'form': form, 'blogs':blogs})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        blogs = Blog.objects.all().order_by('-created_at')[:1]
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog created successfully')
            return redirect(self.success_url)
        return render(request, 'create_blog.html', {'form': form, 'blogs':blogs})

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
    def get(self,request, *args, **kwargs):
        blog = get_object_or_404(Blog,id=kwargs['pk'])
        comment = blog.comments.all()
        form  = CommentForm()

        return render (request,'blog_detail.html',{'blog':blog, 'comment':comment, 'form':form}) 


    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog,id=kwargs['pk'])
        
        form  = CommentForm(request.POST)

        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to post a comment.")
            return redirect('accounts:login')
        
        if form.is_valid():
            comment=form.save(commit=False)
            comment.blog=blog
            comment.user=request.user
            comment.save()
            messages.success(request, "Comment posted successfully.")
            return redirect('blog:blog_detail', pk=blog.pk)
        
        comment = blog.comments.filter(parent__isnull=True)
        return render (request,'blog_detail.html',{'blog':blog, 'comment':comment, 'form':form}) 
    

class AllBlogListView(View):
    template_name =  "templates/blog_list.html"

    def get(self, request, *args, **kwargs):
        blog_list = Blog.objects.all().order_by('-created_at')
        return render(request, 'blog_list.html',{'blog_list':blog_list})   