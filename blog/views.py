# blog/views.py

from django.views import View
from django.views.generic import FormView
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog, Comment
from .forms import BlogForm, CommentForm

class BlogListView(View):
    template_name = 'templates/home.html'
    form_class = BlogForm


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        blogs = Blog.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'blogs': blogs, 'form':form})

class BlogCreateView(LoginRequiredMixin, View):
    template_name = 'templates/create_blog.html'
    form_class = BlogForm
    success_url = 'blog:home'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        blogs = Blog.objects.all().order_by('-created_at')[:1]
        return render(request, 'create_blog.html', {'form': form, 'blogs':blogs})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        blogs = Blog.objects.all().order_by('-created_at')[:1]
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog created successfully')
            return redirect(self.success_url)
        return render(request, 'create_blog.html', {'form': form, 'blogs':blogs})

class BlogUpdateView(LoginRequiredMixin, View):
    template_name = 'templates/blog_update.html'
    form_class = BlogForm
    success_url = 'blog:home'

    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        blogs = Blog.objects.all().order_by('-created_at')[:1]
        form = self.form_class(instance=blog)
        return render(request, 'blog_update.html', {'form': form, 'blogs':blogs})

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        blogs = Blog.objects.all().order_by('-created_at')[:1]
        form = self.form_class(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog updated successfully')
            return redirect('blog:all_blog')
        return render(request, 'blog_update.html', {'form': form, 'blogs':blogs})


class BlogDeleteView(LoginRequiredMixin, View):
    success_url = 'blog:all_blog'

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

class MyBlogView(View):
    template_name = "templates/my_blog.html" 

    def get(self,request, *args, **kwargs):
        blogs = Blog.objects.filter(author=request.user).order_by('-created_at')
        return render(request, 'my_blog.html',{'blogs':blogs})

class CommentReplyView(LoginRequiredMixin, FormView):
    form_class = CommentForm
    template_name = 'blog/comment_reply.html' 
    success_url = '/' 

    def form_valid(self, form):
        blog = get_object_or_404(Blog, pk=self.kwargs['blog_id'])
        parent_comment = get_object_or_404(Comment, pk=self.kwargs['parent_id'])

        reply = form.save(commit=False)
        reply.blog = blog
        reply.user = self.request.user
        reply.parent = parent_comment
        reply.save()

        return redirect('blog:blog_detail', pk=blog.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['blog_id'])
        return context
