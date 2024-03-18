from django.shortcuts import render, get_object_or_404

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

from .models import Conversation, Message

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class IndexView(TemplateView):
    template_name = "chatGPT/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversations = Conversation.objects.all().order_by('-created_at')
        context['conversations'] = conversations
        
        selected_conversation_id = self.request.GET.get('conversation_id')
        if selected_conversation_id:
            selected_conversation = get_object_or_404(Conversation, id=selected_conversation_id)
        else:
            selected_conversation = conversations.first() if conversations.exists() else None

        context['selected_conversation'] = selected_conversation
        return context

class ChatView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ChatSerializer(data=request.data)

        if serializer.is_valid():
            user_message = serializer.validated_data['message']
            conversation_id = serializer.validated_data.get('conversation_id')
                
            # Retrieve the existing conversation using the ID
            conversation = get_object_or_404(Conversation, id=conversation_id)
            
            # Save the user's message
            Message.objects.create(conversation=conversation, text=user_message, is_user_message=True)
            
            # Generate the response from gpt-4
            response = self.chatGPT_call(conversation)
            response = response.choices[0].message.content
            
            # Save the gpt-4's response
            Message.objects.create(conversation=conversation, text=response, is_user_message=False)
            
            return Response({"reply": response})

        return Response(serializer.errors)
        
    def chatGPT_call(self, conversation):
        """
        Returns gpt-4's response to user message
        """
        # Retrieve all messages for the conversation, ordered by creation time
        messages = conversation.messages.all().order_by('created_at')

        # Format messages for the API call. Adjust the format as needed.
        formatted_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]
        for message in messages:
            role = "user" if message.is_user_message else "assistant"
            formatted_messages.append({
                "role": role,
                "content": message.text
            })

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=formatted_messages
            )
            logger.info(response)
        except Exception as e: 
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return response