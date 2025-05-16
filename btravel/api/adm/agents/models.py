from django.db import models
from pgvector.django import VectorField
import uuid
from utils.embeddings import get_embedding

# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    required_fields = models.JSONField(default=list, blank=True)
    optional_fields = models.JSONField(default=list, blank=True)
    prompts = models.JSONField(default=dict, blank=True)
    embedding = VectorField(dimensions=1536, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Generate embedding before saving
        embedding_vector = get_embedding(self.description)
        self.embedding = embedding_vector
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name


class Conversation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    collected_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Conversation {self.id}"
    
    def get_messages(self):
        return self.messages.all()
    
    def get_last_message(self):
        return self.messages.order_by('-created_at').first()
    
    def get_last_user_message(self):
        return self.messages.filter(role='user').order_by('-created_at').first()
    


class Message(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    )
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message {self.id} from {self.conversation.id}"
    
    
    