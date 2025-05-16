from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from pgvector.django import L2Distance
from django.db.models import F

from .models import Agent, Conversation, Message
from ..utlils.embeddings import get_embedding

class ConversationView(APIView):
    """
    API endpoint for handling conversational interactions with agents.
    """
    
    def post(self, request, format=None):
        """
        Process user message, find appropriate agent, and generate response.
        
        - Creates a new conversation if conversation_id is not provided
        - Checks if conversation is still active (within 1 hour)
        - Finds best matching agent using vector similarity
        - Returns agent response and conversation details
        """
        # Get required data from request
        user_message = request.data.get('message')
        conversation_id = request.data.get('conversation_id')
        
        if not user_message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if conversation exists and is active
        conversation = None
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                # Check if conversation is expired (more than 1 hour old)
                one_hour_ago = timezone.now() - timedelta(hours=1)
                if conversation.created_at < one_hour_ago:
                    conversation.is_active = False
                    conversation.save()
                    return Response({
                        'error': 'Conversation has expired',
                        'telegram_link': 'https://t.me/qnbq_assistant_bot/btravel'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Conversation.DoesNotExist:
                return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create new conversation if needed
        if not conversation:
            conversation = Conversation.objects.create()
        
        # Save user message
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        # Find the best agent if none is assigned yet
        if not conversation.agent:
            # Generate embedding for user message
            query_embedding = get_embedding(user_message)
            
            # Find most similar agent
            agents = Agent.objects.annotate(
                distance=L2Distance('embedding', query_embedding)
            ).order_by('distance')
            
            if agents.exists():
                best_agent = agents.first()
                conversation.agent = best_agent
                conversation.save()
            else:
                # Fallback to generic agent if no agents available
                generic_agent = Agent.objects.filter(type='generic').first()
                if not generic_agent:
                    generic_agent = Agent.objects.create(
                        name='Generic Assistant',
                        type='generic',
                        description='I am a general travel assistant who can help you with various travel needs.'
                    )
                conversation.agent = generic_agent
                conversation.save()
        
        # Generate response based on the agent
        agent = conversation.agent
        
        # Check conversation state to determine which questions to ask
        # For simplicity, we're just using a basic response here
        # In a real implementation, you'd want to use LLM to generate responses
        # and track which fields have been collected
        
        # Generate agent response based on collected data and remaining fields
        response_message = self._generate_response(conversation, agent)
        
        # Save assistant message
        assistant_message = Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=response_message
        )
        
        # Check if conversation is complete
        is_complete = self._check_conversation_complete(conversation)
        
        # Return response with conversation details
        return Response({
            'conversation_id': conversation.id,
            'message': response_message,
            'is_complete': is_complete,
            'agent_type': agent.type,
            'telegram_link': 'https://t.me/qnbq_assistant_bot/btravel' if is_complete else None
        })
    
    def _generate_response(self, conversation, agent):
        """
        Generate a response based on the conversation history and agent type.
        In a production system, this would use an LLM to generate responses.
        """
        # Get conversation history
        messages = conversation.get_messages().order_by('created_at')
        
        # For simplicity, using basic logic - in production, use LLM
        if messages.count() <= 1:  # Only user message exists
            return f"Hello! I'm your {agent.type} booking assistant. How can I help you today?"
        
        # Simulate asking for required fields based on agent type
        if agent.type == 'hotel':
            return "Can you tell me your destination, check-in date, check-out date, and number of guests for your hotel booking?"
        elif agent.type == 'apartment':
            return "For apartment booking, I need to know your destination, dates, and how many people will be staying."
        elif agent.type == 'activity':
            return "What type of activity are you interested in, and where? When would you like to do this?"
        elif agent.type == 'tour':
            return "What kind of tour are you looking for? Where would you like to go and for how long?"
        elif agent.type == 'car':
            return "For car rental, I need to know your pickup location, dates, and preferred car type."
        else:
            return "How can I help with your travel plans today?"
    
    def _check_conversation_complete(self, conversation):
        """
        Check if all required information has been collected.
        In a production system, this would analyze the conversation 
        to determine if all required fields were collected.
        """
        # For simplicity, we'll consider a conversation complete after 5 messages
        message_count = conversation.get_messages().count()
        return message_count >= 5
