
from django.urls import path
from .views import ChatView, chatbot_page

urlpatterns = [
    path('', chatbot_page, name='chatbot'),
    path('api/', ChatView.as_view(), name='chatbot_api'),
]
