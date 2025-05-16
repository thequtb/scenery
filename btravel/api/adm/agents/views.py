from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from pgvector.django import L2Distance
from django.db.models import F

from .models import Agent, Conversation, Message
from .serializers import ConversationSerializer
from utils.embeddings import get_embedding
from .langchain_handler import LangChainHandler

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
        - Uses LangChain to process the conversation and extract information
        - Returns agent response and conversation details
        """
        # Validate input data
        serializer = ConversationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated data
        user_message = serializer.validated_data['message']
        conversation_id = serializer.validated_data.get('conversation_id')
        
        # Check if conversation exists and is active
        conversation = None
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                # Check if conversation is expired (more than 1 hour old)
                one_hour_ago = timezone.now() - timedelta(hours=1)
                if conversation.created_at < one_hour_ago or not conversation.is_active:
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
                # Fallback to create a generic agent if none exist
                generic_agent = Agent.objects.create(
                    name='Generic Travel Assistant',
                    description='I am a general travel assistant that can help with various travel needs.',
                    required_fields=['travel_type', 'destination', 'dates', 'travelers'],
                    optional_fields=['budget', 'preferences', 'special_requirements'],
                    prompts={
                        'travel_type': 'What type of travel assistance do you need?',
                        'destination': 'Where are you planning to travel?',
                        'dates': 'When are you planning to travel?',
                        'travelers': 'How many people are traveling?'
                    }
                )
                conversation.agent = generic_agent
                conversation.save()
        
        # Process message with LangChain
        agent = conversation.agent
        langchain_handler = LangChainHandler(agent, conversation)
        result = langchain_handler.process_message(user_message)
        
        # Extract response components
        response_message = result.get('response', "I'm here to help with your travel plans.")
        is_complete = result.get('is_complete', False)
        
        # Save assistant message
        Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=response_message
        )
        
        # Return response with conversation details
        return Response({
            'conversation_id': conversation.id,
            'message': response_message,
            'is_complete': is_complete,
            'telegram_link': 'https://t.me/qnbq_assistant_bot/btravel' if is_complete else None
        })
