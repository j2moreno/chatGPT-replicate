from django.db import models
import uuid

# class Conversation(models.Model):
#     session_id = models.UUIDField(default=uuid.uuid4, editable=False)
#     question = models.TextField()
#     answer = models.TextField(blank=True, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Conversation {self.session_id} at {self.timestamp}"
