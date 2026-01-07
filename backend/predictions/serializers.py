from rest_framework import serializers
from .models import Prediction, SurveyAnswer

class SurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswer
        exclude = ['id', 'prediction'] 

class PredictionSerializer(serializers.ModelSerializer):
    answers = SurveyAnswerSerializer(read_only=True)

    class Meta:
        model = Prediction
        fields = ['id', 'user', 'risk_score', 'created_at', 'answers']
        read_only_fields = ['user', 'risk_score', 'created_at']