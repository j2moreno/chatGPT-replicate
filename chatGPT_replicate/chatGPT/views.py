from django.shortcuts import render

# Create your views here.
from django.conf import settings
from openai import OpenAI

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ChatSerializer
from django.views.generic import TemplateView

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class IndexView(TemplateView):
    template_name = "chatGPT/index.html"

class ChatView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            user_message = serializer.validated_data['message']
            
            response = client.completions.create(
                model="gpt-4",
                prompt=user_message,
                temperature=0.7,
                max_tokens=150
            )
            return Response({"reply": response.choices[0].text.strip()})
        return Response(serializer.errors, status=400)
