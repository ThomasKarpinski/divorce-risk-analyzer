from django.urls import path
from predictions.views import register_user, login_user

urlpatterns = [
    path('register/', register_user, name='api_register'),
    path('login/', login_user, name='api_login'),
]
