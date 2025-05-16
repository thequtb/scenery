import os
import json
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_embedding(text, model="text-embedding-3-small"):
    """
    Get OpenAI embedding for the provided text
    
    Args:
        text (str): The text to embed
        model (str): The embedding model to use
        
    Returns:
        numpy.ndarray: The embedding vector
    """
    if not text:
        # Return zero vector if text is empty
        return np.zeros(1536)
        
    # Clean and prepare text
    text = text.replace("\n", " ")
    
    # Get embeddings from OpenAI
    response = client.embeddings.create(
        input=text,
        model=model
    )
    
    # Extract embedding and convert to numpy array
    embedding_vector = response.data[0].embedding
    
    return np.array(embedding_vector)

def generate_bookable_embedding(title, type_value, destination_name, options):
    """
    Generate embedding for a Bookable item
    
    Args:
        title (str): Bookable title
        type_value (str): Bookable type
        destination_name (str): Name of the destination
        options (dict): Options dictionary
        
    Returns:
        numpy.ndarray: The embedding vector
    """
    # Combine the text
    options_text = json.dumps(options) if options else "{}"
    combined_text = f"Title: {title}. Type: {type_value}. Destination: {destination_name}. Options: {options_text}"
    
    return get_embedding(combined_text)

def generate_collection_embedding(description):
    """
    Generate embedding for a Collection
    
    Args:
        description (str): Collection description
        
    Returns:
        numpy.ndarray: The embedding vector
    """
    return get_embedding(description) 