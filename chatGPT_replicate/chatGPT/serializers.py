from rest_framework import serializers

class ChatSerializer(serializers.Serializer):
    message = serializers.CharField()
    conversation_id = serializers.IntegerField()
