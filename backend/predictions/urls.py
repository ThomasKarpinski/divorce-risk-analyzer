from django.urls import path
from .views import PredictView, calculate_statistic

urlpatterns = [
    path('submit/', PredictView.as_view(), name='submit-prediction'),
    path('stats/', calculate_statistic, name='calculate_statistic'),
]