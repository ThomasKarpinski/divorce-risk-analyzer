from django.contrib import admin
from .models import Prediction, SurveyAnswer

class SurveyAnswerInline(admin.StackedInline):
    model = SurveyAnswer
    can_delete = False
    verbose_name_plural = 'Answers'

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'risk_score', 'created_at')
    list_filter = ('created_at',)
    inlines = [SurveyAnswerInline]