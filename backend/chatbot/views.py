import logging
import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _, get_language
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Models
from predictions.models import Prediction, SurveyAnswer
from core.models import DivorceData
from .models import ChatMessage

# LangChain Imports
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

# Configuration
OLLAMA_BASE_URL = "http://ollama:11434"
MODEL_NAME = "llama3.2:1b"

logger = logging.getLogger(__name__)

@login_required
def chatbot_page(request):
    messages = ChatMessage.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'chatbot.html', {'messages': messages})

class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_context_from_prediction(self, user):
        """Helper to generate context string from the latest survey prediction."""
        latest_prediction = Prediction.objects.filter(user=user).order_by('-created_at').first()
        if not latest_prediction:
            return ""

        context_str = f"User Risk Score: {latest_prediction.risk_score:.1%}. "
        
        try:
            answers = latest_prediction.answers
            specifics = []

            def get_q_text(q_key):
                try:
                    return DivorceData._meta.get_field(q_key).verbose_name
                except:
                    return f"Question {q_key}"

            # 1. Critical Questions Check
            q11 = getattr(answers, 'q11', 4) # Harmony
            q17 = getattr(answers, 'q17', 4) # Happiness views
            q40 = getattr(answers, 'q40', 0) # Arguments

            critical_issues = []
            if q11 <= 1: critical_issues.append(_("Low harmony (Score: {score}/4).").format(score=q11))
            if q17 <= 1: critical_issues.append(_("Different happiness views (Score: {score}/4).").format(score=q17))
            if q40 >= 3: critical_issues.append(_("Sudden arguments (Score: {score}/4).").format(score=q40))

            if critical_issues:
                context_str += _("CRITICAL THREAT FACTORS: ") + " ".join(critical_issues)
            else:
                # 2. General Analysis (Restored Logic)
                # Positive Questions (Should be high): Q1-Q30
                worst_positive = None
                min_pos_val = 5
                for i in range(1, 31):
                    q_key = f'q{i}'
                    val = getattr(answers, q_key, 4)
                    if val < min_pos_val:
                        min_pos_val = val
                        worst_positive = (q_key, val)
                
                # Negative Questions (Should be low): Q31-Q54
                worst_negative = None
                max_neg_val = -1
                for i in range(31, 55):
                    q_key = f'q{i}'
                    val = getattr(answers, q_key, 0)
                    if val > max_neg_val:
                        max_neg_val = val
                        worst_negative = (q_key, val)

                findings = []
                if worst_positive and worst_positive[1] <= 2:
                    q_text = get_q_text(worst_positive[0])
                    findings.append(_("Main Area of Neglect: '{question}' (Score: {score}/4 - Too Low).").format(question=q_text, score=worst_positive[1]))
                
                if worst_negative and worst_negative[1] >= 2:
                    q_text = get_q_text(worst_negative[0])
                    findings.append(_("Main Conflict Source: '{question}' (Score: {score}/4 - Too High).").format(question=q_text, score=worst_negative[1]))

                if findings:
                    context_str += _(" SPECIFIC AREAS TO DISCUSS: ") + " ".join(findings)

        except SurveyAnswer.DoesNotExist:
            pass
            
        return context_str

    def _get_langchain_history(self, user):
        """Retrieve last 4 messages from Django ORM and convert to LangChain format."""
        # Get last 4 messages (ordered by creation)
        db_messages = ChatMessage.objects.filter(user=user).order_by('-created_at')[:4]
        # Reverse to get chronological order [Oldest -> Newest]
        db_messages = reversed(db_messages)
        
        history = []
        for msg in db_messages:
            if msg.role == 'user':
                history.append(HumanMessage(content=msg.content))
            elif msg.role == 'assistant':
                history.append(AIMessage(content=msg.content))
        return history

    def post(self, request):
        user_message = request.data.get('message')
        if not user_message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        #  Preparation of context
        survey_context = self._get_context_from_prediction(request.user)
        chat_history = self._get_langchain_history(request.user)
        
        # Get current language
        lang_code = get_language()
        lang_map = {
            'pl': 'Polish',
            'en': 'English',
            'en-us': 'English',
            'en-gb': 'English'
        }
        target_language = lang_map.get(lang_code.lower(), 'English')
        
        lang_instruction = f"IMPORTANT: You MUST answer in {target_language} language only."

        # Defining System Prompt with Chain of Thought
        system_prompt_text = (
            "You are a helpful and empathetic relationship counselor AI (Gottman Method).\n"
            f"{lang_instruction}\n"
            "Below is the data from the user's divorce risk survey. You MUST memorize this:\n\n"
            
            f"=== SURVEY_DATA ===\n{survey_context}\n===================\n\n"
            
            "INSTRUCTIONS:\n"
            "1. If the user asks about the survey/results, refer explicitly to the SURVEY_DATA above.\n"
            "2. If the user chats casually, answer normally but keep the survey data in mind as background context.\n"
            "3. CHAIN OF THOUGHT: Before answering, think inside <thought> tags:\n"
            "   - Does the user's question relate to the survey?\n"
            "   - If yes -> look up the specific question in SURVEY_DATA.\n"
            "   - Draft the response.\n"
            "4. Keep response short (max 3 sentences) and supportive.\n"
            f"5. REMEMBER: Answer in {target_language}."
        )

        # Setup LangChain
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt_text),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])

        llm = ChatOllama(
            base_url=OLLAMA_BASE_URL,
            model=MODEL_NAME,
            temperature=0.7,
            keep_alive="5m"
        )

        chain = prompt | llm | StrOutputParser()

        try:
            # Saving User Message to DB (Django ORM)
            ChatMessage.objects.create(user=request.user, role='user', content=user_message)

            # We pass the converted history and the new input
            response_text = chain.invoke({
                "history": chat_history,
                "input": user_message
            })
            
            # Robust filtering of <thought> tags using regex
            final_response = re.sub(r'<thought>.*?</thought>', '', response_text, flags=re.DOTALL).strip()

            # 7. Save AI Message to DB (Django ORM)
            ChatMessage.objects.create(user=request.user, role='assistant', content=final_response)

            return Response({'response': final_response}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"LangChain Error: {e}")
            return Response({'error': f"AI processing failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
