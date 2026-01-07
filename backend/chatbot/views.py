import requests
import json
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from predictions.models import Prediction, SurveyAnswer
from core.models import DivorceData

OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

def chatbot_page(request):
    return render(request, 'chatbot.html')

class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('message')
        if not user_message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get latest prediction for context
        latest_prediction = Prediction.objects.filter(user=request.user).order_by('-created_at').first()
        
        context = ""
        if latest_prediction:
            context = f"The user has completed a divorce risk survey. Their calculated risk score is {latest_prediction.risk_score:.1%}. "
            
            try:
                answers = latest_prediction.answers
                specifics = []

                # Helper to get question text
                def get_question_text(q_key):
                    field = DivorceData._meta.get_field(q_key)
                    return field.verbose_name

                # Critical Questions (Q11, Q17, Q40)
                # Bad if Q11 low, Q17 low, Q40 high
                q11_val = getattr(answers, 'q11')
                q17_val = getattr(answers, 'q17')
                q40_val = getattr(answers, 'q40')

                critical_issues = []
                if q11_val <= 1:
                    critical_issues.append(f"Low harmony (Q11: {q11_val}/4).")
                if q17_val <= 1:
                    critical_issues.append(f"Different views on happiness (Q17: {q17_val}/4).")
                if q40_val >= 3:
                    critical_issues.append(f"Sudden arguments (Q40: {q40_val}/4).")

                if critical_issues:
                    # If critical issues found, focus ONLY on them
                    context += "CRITICAL ISSUES IDENTIFIED: " + " ".join(critical_issues) + " Focus advice on these specific critical problems."
                
                else:
                    # General Analysis (Secondary Method)
                    # Only if no critical issues found
                    
                    positive_set = [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
                    negative_set = [6, 7, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]

                    # Find Lowest value in Positive Set
                    worst_positive = None
                    min_pos_val = 5
                    for q_num in positive_set:
                        q_key = f'q{q_num}'
                        val = getattr(answers, q_key)
                        if val < min_pos_val:
                            min_pos_val = val
                            worst_positive = (q_key, val)
                    
                    # Finding Highest value in Negative Set
                    worst_negative = None
                    max_neg_val = -1
                    for q_num in negative_set:
                        q_key = f'q{q_num}'
                        val = getattr(answers, q_key)
                        if val > max_neg_val:
                            max_neg_val = val
                            worst_negative = (q_key, val)

                    # Adding findings to context
                    if worst_positive:
                        q_text = get_question_text(worst_positive[0])
                        specifics.append(f"Weakest Positive Area: '{q_text}' (Score: {worst_positive[1]}/4).")
                    
                    if worst_negative:
                        q_text = get_question_text(worst_negative[0])
                        specifics.append(f"Strongest Negative Issue: '{q_text}' (Score: {worst_negative[1]}/4).")

                    if specifics:
                        context += " KEY AREAS FOR IMPROVEMENT: " + " ".join(specifics)

            except SurveyAnswer.DoesNotExist:
                pass
            
            system_prompt = (
                        "You are a helpful relationship counselor assistant. "
                        "Your goal is to provide supportive, non-judgmental advice. "
                        "IMPORTANT: Keep your answers CONCISE and SHORT (max 3-4 sentences). "
                        "Focus directly on the user's question. Do not ramble. "
                        "If the risk is high, briefly encourage professional therapy. "
                        f"Context: {context}"
                    )

        prompt = f"{system_prompt}\nUser: {user_message}\nAssistant:"

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "keep_alive": "5m",
            "options": {
                "num_predict": 256,
                "temperature": 0.7
            }
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=300)
            response.raise_for_status()
            ai_response = response.json().get('response')
            return Response({'response': ai_response}, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to connect to Ollama: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
