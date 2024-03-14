from django.shortcuts import render

# Create your views here.
from django.conf import settings
from openai import OpenAI
import openai

import logging 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ChatSerializer
from django.views.generic import TemplateView

#from .models import Conversation

#client = OpenAI(api_key=settings.OPENAI_API_KEY)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class IndexView(TemplateView):
    template_name = "chatGPT/index.html"

class ChatView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ChatSerializer(data=request.data)

        # session_id = request.data.get('session_id')
        # question = request.data.get('question')
        
        # # Fetch conversation history
        # history = Conversation.objects.filter(session_id=session_id).order_by('timestamp')
        
        # # Compile history into a single string or structured format your model expects
        # history_text = "\n".join([f"Q: {conv.question}\nA: {conv.answer}" for conv in history])
        

        if serializer.is_valid():
            user_message = serializer.validated_data['message']
    
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": user_message}
                    ]
                )
                logger.info(response)
            except Exception as e: 
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"reply": response.choices[0].message.content})
        
        return Response(serializer.errors, status=400)
