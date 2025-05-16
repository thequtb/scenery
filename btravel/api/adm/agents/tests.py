from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
import uuid
from unittest.mock import patch, MagicMock
import json

from .models import Agent, Conversation, Message

class ConversationAPITests(APITestCase):
    
    def setUp(self):
        # Create test agent
        self.agent = Agent.objects.create(
            name="Test Agent",
            description="I am a test agent for travel assistance."
        )
        
        # Setup API client
        self.client = APIClient()
        self.url = reverse('conversation')
        
    @patch('agents.views.LangChainHandler')
    def test_new_conversation_creation(self, mock_langchain):
        """Test creating a new conversation with initial message"""
        # Mock langchain response
        mock_instance = mock_langchain.return_value
        mock_instance.process_message.return_value = {
            'response': 'Hello! How can I help with your travel plans?',
            'extracted_fields': {},
            'is_complete': False
        }
        
        # Send initial message
        data = {'message': 'I need help booking a hotel'}
        response = self.client.post(self.url, data, format='json')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('conversation_id', response.data)
        self.assertIn('message', response.data)
        self.assertFalse(response.data['is_complete'])
        
        # Verify conversation was created
        conversation_id = response.data['conversation_id']
        self.assertTrue(Conversation.objects.filter(id=conversation_id).exists())
        
        # Verify message was saved
        conversation = Conversation.objects.get(id=conversation_id)
        self.assertEqual(conversation.messages.count(), 2)  # User message + assistant response
        
        # Verify langchain was called with correct data
        mock_instance.process_message.assert_called_once()
    
    @patch('agents.views.LangChainHandler')
    def test_continuing_conversation(self, mock_langchain):
        """Test continuing an existing conversation"""
        # Create a conversation
        conversation = Conversation.objects.create()
        Message.objects.create(
            conversation=conversation,
            role='user',
            content='Initial message'
        )
        Message.objects.create(
            conversation=conversation,
            role='assistant',
            content='Initial response'
        )
        
        # Mock langchain response
        mock_instance = mock_langchain.return_value
        mock_instance.process_message.return_value = {
            'response': 'I can help with that. When are you planning to travel?',
            'extracted_fields': {'destination': 'New York'},
            'is_complete': False
        }
        
        # Send follow-up message
        data = {
            'message': 'I want to go to New York',
            'conversation_id': str(conversation.id)
        }
        response = self.client.post(self.url, data, format='json')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['conversation_id']), str(conversation.id))
        self.assertEqual(response.data['message'], 'I can help with that. When are you planning to travel?')
        
        # Verify messages were saved
        conversation.refresh_from_db()
        self.assertEqual(conversation.messages.count(), 4)  # 2 initial + new user message + new response
        
    @patch('agents.views.LangChainHandler')
    def test_conversation_completion(self, mock_langchain):
        """Test completion of conversation"""
        # Create a conversation
        conversation = Conversation.objects.create()
        
        # Mock langchain response indicating completion
        mock_instance = mock_langchain.return_value
        mock_instance.process_message.return_value = {
            'response': 'Great! I have all the information I need.',
            'extracted_fields': {'destination': 'Paris', 'dates': 'Next weekend', 'travelers': '2'},
            'is_complete': True
        }
        
        # Send message
        data = {
            'message': 'We want to travel to Paris next weekend, just me and my wife',
            'conversation_id': str(conversation.id)
        }
        response = self.client.post(self.url, data, format='json')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_complete'])
        self.assertEqual(response.data['telegram_link'], 'https://t.me/qnbq_assistant_bot/btravel')
        
    def test_expired_conversation(self):
        """Test handling expired conversation"""
        # Create an expired conversation (will be mocked with a pre-set is_active=False)
        expired_conversation = Conversation.objects.create(is_active=False)
        
        # Send message to expired conversation
        data = {
            'message': 'Hello again',
            'conversation_id': str(expired_conversation.id)
        }
        response = self.client.post(self.url, data, format='json')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('telegram_link', response.data)
    
    def test_invalid_data(self):
        """Test handling invalid request data"""
        # Missing message
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Invalid conversation ID
        data = {'message': 'Test', 'conversation_id': 'not-a-uuid'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
