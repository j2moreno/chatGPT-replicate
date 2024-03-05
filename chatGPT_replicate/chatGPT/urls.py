from django.urls import path
from .views import ChatView, IndexView

app_name = "chatGPT"
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('chat/', ChatView.as_view(), name='chat'),
]
