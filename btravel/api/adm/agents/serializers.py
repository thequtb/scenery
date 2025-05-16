from rest_framework import serializers
import uuid

class ConversationSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, help_text="User message")
    conversation_id = serializers.UUIDField(required=False, help_text="Existing conversation ID")
    
    def validate_message(self, value):
        """
        Validate user message.
        """
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value
    
    def validate_conversation_id(self, value):
        """
        Validate conversation ID format.
        """
        try:
            return uuid.UUID(str(value))
        except (ValueError, AttributeError):
            raise serializers.ValidationError("Invalid conversation ID format")

class MessageSerializer(serializers.Serializer):
    role = serializers.CharField()
    content = serializers.CharField()
    
    def validate_role(self, value):
        """
        Validate message role.
        """
        valid_roles = ['user', 'assistant', 'system']
        if value not in valid_roles:
            raise serializers.ValidationError(f"Role must be one of: {', '.join(valid_roles)}")
        return value 