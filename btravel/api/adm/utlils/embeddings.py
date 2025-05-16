import os
import numpy as np
from openai import OpenAI

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

