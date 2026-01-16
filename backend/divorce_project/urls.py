from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from core.views import home
from users.views import register_view, login_view
from predictions.views import survey_view, result_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register_view, name='register'),
    path('survey/', survey_view, name='survey'),
    path('result/', result_view, name='result'),
    
    # API endpoints
    path('api/', include('predictions.urls')),
    path('api/users/', include('users.urls')),
    path('api/chatbot/', include('chatbot.urls')),
]