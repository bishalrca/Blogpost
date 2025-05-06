from django.urls import path
from .views import CustomLoginView, CustomLogoutView, SignupView, ProfileView, ProfileEditView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/',ProfileEditView.as_view(), name='profile_edit'),
]
