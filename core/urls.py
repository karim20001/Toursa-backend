from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import SignUpView, LoginView, LogoutView, ProfileView, TokenVerifyView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify-token/', TokenVerifyView.as_view(), name='verify-token'),
]
