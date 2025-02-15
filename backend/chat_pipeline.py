import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Gemini client
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_chat_response(text, context=""):
    """
    Get a response from Gemini for the given text and context.
    
    Args:
        text (str): The user's input text
        context (str): Optional context to help guide the response
        
    Returns:
        dict: {
            'success': bool,
            'response': str,  # The chat response if successful
            'error': str     # Error message if not successful
        }
    """
    try:
        logger.info("Sending request to Gemini")
        
        # Create the model
        model = genai.GenerativeModel('gemini-pro')
        
        # System prompt to set behavior
        system_prompt = """You are an AI assistant that:
        1. Specializes in analyzing and explaining code repositories
        2. Speaks in a natural, conversational way
        3. References specific parts of the code when relevant
        4. Keeps responses clear and concise
        
        When analyzing repositories:
        - Point out interesting patterns or design choices
        - Explain technical concepts in simple terms
        - Use examples from the actual codebase
        """
        
        # Combine system prompt, context, and user question
        full_prompt = f"""{system_prompt}

        Repository Context:
        {context}

        User Question: {text}"""
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        logger.info("Received response from Gemini")
        return {
            'success': True,
            'response': response.text
        }
    except Exception as e:
        logger.error(f"Gemini request failed: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    # Test the chat pipeline
    test_input = "What are the key principles of clean code?"
    test_context = "We are discussing software development best practices."
    
    logger.info(f"Testing chat pipeline with input: {test_input}")
    result = get_chat_response(test_input, test_context)
    
    if result['success']:
        print("\n=== Chat Response ===")
        print(result['response'])
        print("\n=== End of Response ===")
    else:
        logger.error(f"Test failed: {result['error']}") 