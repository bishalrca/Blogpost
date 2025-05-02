
from .models import Blog

def latest_blog(request):
    try:
        blog = Blog.objects.latest('created_at')
    except Blog.DoesNotExist:
        blog = None
    return {'latest_blog': blog}
