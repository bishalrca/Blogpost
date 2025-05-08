
from django.urls import path
from .views import BlogListView, BlogCreateView, BlogUpdateView, BlogDeleteView, BlogDetailView, AllBlogListView, MyBlogView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('create/', BlogCreateView.as_view(), name='create_blog'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='update_blog'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/list/', AllBlogListView.as_view(), name='all_blog'),
    path('myblog/', MyBlogView.as_view(), name='my_blog'),
]
