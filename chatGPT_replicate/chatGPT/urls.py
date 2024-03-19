from django.urls import path
from .views import ChatView, IndexView, create_conversation

app_name = "chatGPT"
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('create_conversation/', create_conversation, name='create_conversation'),
]
