import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from .models import Agent, Conversation, Message

class LangChainHandler:
    """Handler for LangChain conversations with agents"""
    
    def __init__(self, agent, conversation):
        """
        Initialize LangChain handler
        
        Args:
            agent: The Agent model instance
            conversation: The Conversation model instance
        """
        self.agent = agent
        self.conversation = conversation
        self.llm = ChatOpenAI(temperature=0.7)
        
    def _build_prompt(self, messages):
        """
        Build the prompt from conversation history.
        
        Args:
            messages: List of Message model instances
        
        Returns:
            List of langchain message objects
        """
        langchain_messages = []
        
        # Add system prompt with agent description and fields to collect
        system_prompt = (
            f"{self.agent.description}\n\n"
            f"Required fields to collect: {', '.join(self.agent.required_fields)}\n"
            f"Optional fields to collect: {', '.join(self.agent.optional_fields)}\n\n"
            "Instructions:\n"
            "1. Be conversational and helpful\n"
            "2. Ask for required fields first, then optional fields\n"
            "3. Extract information from user messages\n"
            "4. Keep track of what information you've collected\n"
            "5. When all required fields are collected, indicate completion\n"
        )
        langchain_messages.append(SystemMessage(content=system_prompt))
        
        # Add conversation history
        for msg in messages:
            if msg.role == 'user':
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == 'assistant':
                langchain_messages.append(AIMessage(content=msg.content))
        
        # Add context about collected data so far
        if self.conversation.collected_data:
            data_summary = "Information collected so far:\n"
            for field, value in self.conversation.collected_data.items():
                data_summary += f"- {field}: {value}\n"
            
            remaining = [f for f in self.agent.required_fields if f not in self.conversation.collected_data]
            if remaining:
                data_summary += f"\nStill need to collect: {', '.join(remaining)}\n"
            
            langchain_messages.append(SystemMessage(content=data_summary))
        
        return langchain_messages
    
    def _create_output_parser(self):
        """
        Create an output parser for structured responses.
        
        Returns:
            StructuredOutputParser instance
        """
        # Define schemas for the expected outputs
        response_schema = ResponseSchema(
            name="response",
            description="The conversational response to send to the user"
        )
        
        extracted_fields_schema = ResponseSchema(
            name="extracted_fields",
            description="JSON object with extracted fields from user message"
        )
        
        is_complete_schema = ResponseSchema(
            name="is_complete",
            description="Boolean indicating if all required information has been collected"
        )
        
        # Create the output parser
        return StructuredOutputParser.from_response_schemas([
            response_schema, 
            extracted_fields_schema, 
            is_complete_schema
        ])
    
    def process_message(self, user_message):
        """
        Process a user message using LangChain.
        
        Args:
            user_message: The content of the user's message
            
        Returns:
            Dict with response message, extracted fields, and completion status
        """
        # Get conversation history
        messages = list(self.conversation.get_messages().order_by('created_at'))
        
        # Build the prompt
        prompt_messages = self._build_prompt(messages)
        
        # Create output parser
        output_parser = self._create_output_parser()
        format_instructions = output_parser.get_format_instructions()
        
        # Create the chain
        chat_prompt = ChatPromptTemplate.from_messages([
            *prompt_messages,
            HumanMessage(content=user_message),
            SystemMessage(content=f"Format your response as JSON according to these instructions: {format_instructions}")
        ])
        
        chain = LLMChain(llm=self.llm, prompt=chat_prompt)
        
        # Run the chain
        result = chain.run("")
        
        try:
            # Parse the output
            parsed_output = output_parser.parse(result)
            
            # Update collected data
            if parsed_output.get('extracted_fields'):
                extracted = parsed_output['extracted_fields']
                if isinstance(extracted, str):
                    # Handle case where JSON is returned as string
                    extracted = json.loads(extracted)
                
                # Update conversation's collected data
                current_data = self.conversation.collected_data.copy()
                current_data.update(extracted)
                self.conversation.collected_data = current_data
                self.conversation.save()
            
            return parsed_output
        except Exception as e:
            # Fallback for parsing errors
            return {
                'response': f"I'm here to help with your travel plans. Could you provide more details?",
                'extracted_fields': {},
                'is_complete': False
            } 