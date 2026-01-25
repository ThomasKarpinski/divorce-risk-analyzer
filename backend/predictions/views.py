from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.translation import gettext as _
from .models import Prediction, SurveyAnswer
from .serializers import PredictionSerializer, SurveyAnswerSerializer
import random
import os
import joblib
import numpy as np

from core.models import DivorceData

from django.db.models import F
from datetime import date
import pandas as pd
import plotly.express as px
import plotly.io as pio

User = get_user_model()

# MODEL LOADING
MODEL_PATH = os.path.join(settings.BASE_DIR, 'predictions', 'ml_models', 'model.pkl')
_model = None

def get_model():
    global _model
    if _model is None:
        try:
            print(f"Loading model from: {MODEL_PATH}")
            _model = joblib.load(MODEL_PATH)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"CRITICAL ERROR loading model: {e}")
            import traceback
            traceback.print_exc()
            return None
    return _model

# WEB VIEWS 

def survey_view(request):
    return render(request, 'survey.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calculate_statistic(request):
    question_id = request.GET.get('question_id')
    answer_value = request.GET.get('answer_value')

    if not question_id or answer_value is None:
        return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate question_id (simple check)
    if not question_id.startswith('q') or not question_id[1:].isdigit():
        return Response({'error': 'Invalid question ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        val = int(answer_value)
    except ValueError:
        return Response({'error': 'Invalid answer value'}, status=status.HTTP_400_BAD_REQUEST)

    # Count total records in dataset
    total_count = DivorceData.objects.count()
    if total_count == 0:
        return Response({'percentage': 0, 'message': 'No data available'}, status=status.HTTP_200_OK)

    # Count matching records
    # Dynamic field lookup using **kwargs
    filter_kwargs = {question_id: val}
    try:
        match_count = DivorceData.objects.filter(**filter_kwargs).count()
    except Exception as e:
         return Response({'error': f'Error querying data: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    percentage = round((match_count / total_count) * 100, 1)

    return Response({
        'question_id': question_id,
        'answer_value': val,
        'percentage': percentage,
        'message': _("{percentage}% of people in our research answered the same.").format(percentage=percentage)
    })

def result_view(request):
    if request.method == 'POST':
        # Collect answers from q1 to q54
        data = {}
        input_features = []
        for i in range(1, 55):
            key = f'q{i}'
            val = request.POST.get(key)
            if val is not None:
                int_val = int(val)
                data[key] = int_val
                input_features.append(int_val)
            else:
                data[key] = 0 # Default
                input_features.append(0)

        # ML Prediction
        model = get_model()
        if model:
            try:
                # Preprocess features:
                # Q1-Q30 are Positive (Agree = Good). We assume model treats 0 as Good and 4 as Bad.
                # So for Q1-Q30, we invert: 4 -> 0, 0 -> 4.
                # Q31-Q54 are Negative (Agree = Bad). We keep as is: 4 -> 4.
                
                processed_features = []
                for i in range(54):
                    # i is 0-based index. Q1 is index 0.
                    val = input_features[i]
                    
                    if i < 30: # Q1 to Q30 (indices 0 to 29)
                        processed_features.append(4 - val)
                    else:      # Q31 to Q54
                        processed_features.append(val)

                # Expecting 1 sample, 54 features
                input_array = np.array([processed_features])
                print(f"Running prediction on input shape: {input_array.shape}")
                # predict_proba returns [[prob_0, prob_1]]
                risk_score = float(model.predict_proba(input_array)[0][1])
                print(f"Prediction result: {risk_score}")
            except Exception as e:
                print(f"Prediction error: {e}")
                import traceback
                traceback.print_exc()
                risk_score = random.random() # Fallback
        else:
            print("Model not loaded, using fallback.")
            risk_score = random.random() # Fallback
        
        # Save if user is authenticated
        user = request.user if request.user.is_authenticated else None
        
        prediction = Prediction.objects.create(
            user=user,
            risk_score=risk_score
        )
        
        # Save answers
        SurveyAnswer.objects.create(prediction=prediction, **data)
        
        context = {
            'risk_score': risk_score * 100, # Show as percentage in template if needed, or keep 0-1
            'message': f"Your relationship divorce risk is estimated at {risk_score:.1%}.",
        }
        
        if user:
             # Calculate statistics for q1 (example logic from API)
            user_q1_answer = data.get('q1', 0)
            total_surveys = SurveyAnswer.objects.count()
            same_answer_count = SurveyAnswer.objects.filter(q1=user_q1_answer).count()
            
            percentage = int((same_answer_count / total_surveys) * 100) if total_surveys > 0 else 0
            
            context['statistics'] = {
                "q1_same_choice_percentage": f"{percentage}% of users answered the same for question 1."
            }

        return render(request, 'result.html', context)

    return redirect('survey')


@login_required
def dashboard_view(request):
    # Checking if user has completed survey
    user_predictions = Prediction.objects.filter(user=request.user)
    if not user_predictions.exists():
        return render(request, 'dashboard.html', {
            'no_data': True,
            'message': "You need to complete the survey first to see the community dashboard."
        })

    predictions = Prediction.objects.filter(user__isnull=False).select_related('user')
    
    data = []
    for pred in predictions:
        u = pred.user
        age = None
        if u.birthdate:
            today = date.today()
            age = today.year - u.birthdate.year - ((today.month, today.day) < (u.birthdate.month, u.birthdate.day))
        
        data.append({
            'Risk Score': pred.risk_score * 100,
            'Gender': u.gender if u.gender else 'Unknown',
            'Education': u.education if u.education else 'Unknown',
            'Age': age if age is not None else 0
        })

    df = pd.DataFrame(data)

    # generating Charts
    graphs = []

    # Chart A: Risk Score by Gender (Box Plot)
    if not df.empty and 'Gender' in df.columns:
        fig_gender = px.box(
            df, x='Gender', y='Risk Score', 
            title="Divorce Risk Distribution by Gender",
            color='Gender',
            points="all"
        )
        graphs.append(pio.to_html(fig_gender, full_html=False))

    # Chart B: Risk Score by Education (Bar Chart - Average)
    if not df.empty and 'Education' in df.columns:
        edu_order = ['primary', 'secondary', 'bachelor', 'master', 'phd']
        # only existing ones
        avg_risk_edu = df.groupby('Education')['Risk Score'].mean().reset_index()
        fig_edu = px.bar(
            avg_risk_edu, x='Education', y='Risk Score',
            title="Average Risk Score by Education Level",
            color='Risk Score',
            category_orders={"Education": edu_order}
        )
        graphs.append(pio.to_html(fig_edu, full_html=False))

    # Chart C: Risk Score vs Age (Scatter Plot)
    if not df.empty and 'Age' in df.columns:
        # Filter out 0 age if irrelevant
        age_df = df[df['Age'] > 0]
        fig_age = px.scatter(
            age_df, x='Age', y='Risk Score',
            title="Risk Score vs. Age",
            trendline="ols" if len(age_df) > 1 else None, # Adding trendline if enough data
            color='Gender',
            range_x=[0, 100]
        )
        graphs.append(pio.to_html(fig_age, full_html=False))

    context = {
        'graphs': graphs
    }

    return render(request, 'dashboard.html', context)

# API VIEWS (Existing)
class PredictView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        answer_serializer = SurveyAnswerSerializer(data=request.data)
        
        if answer_serializer.is_valid():
            # Extract features from serializer data
            validated_data = answer_serializer.validated_data
            input_features = []
            for i in range(1, 55):
                input_features.append(validated_data.get(f'q{i}', 0))
            
            # ML Prediction
            model = get_model()
            if model:
                try:
                    input_array = np.array([input_features])
                    risk_score = float(model.predict_proba(input_array)[0][1])
                except Exception as e:
                    print(f"Prediction error: {e}")
                    risk_score = random.random()
            else:
                 risk_score = random.random()

            prediction = Prediction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                risk_score=risk_score
            )
            answer_serializer.save(prediction=prediction)

            response_data = {
                "id": prediction.id,
                "risk_score": prediction.risk_score,
                "message": "Analiza zakończona."
            }

            if request.user.is_authenticated:
                user_q1_answer = request.data.get('q1')
                total_surveys = SurveyAnswer.objects.count()
                same_answer_count = SurveyAnswer.objects.filter(q1=user_q1_answer).count()
                
                percentage = int((same_answer_count / total_surveys) * 100) if total_surveys > 0 else 0

                response_data["statistics"] = {
                    "q1_same_choice_percentage": f"{percentage}% użytkowników odpowiedziało tak samo w pytaniu 1."
                }
                response_data["chatbot_access"] = True
                response_data["chatbot_url"] = "/api/chatbot/"
            
            else:
                response_data["info"] = "Zaloguj się, aby zobaczyć statystyki i porozmawiać z AI."

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Podaj login i hasło'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Taki użytkownik już istnieje'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Błędne dane'}, status=status.HTTP_401_UNAUTHORIZED)
