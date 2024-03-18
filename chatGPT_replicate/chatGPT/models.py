from django.db import models
import uuid

class Conversation(models.Model):
    session_id = models.CharField(max_length=255, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Conversation {self.session_id} at {self.created_at}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()

    # True if the message is from the user, False if from gpt-4
    is_user_message = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def get_css_class(self):
        return 'user-message' if self.is_user_message else 'gpt-message'