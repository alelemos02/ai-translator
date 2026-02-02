import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
try:
    import streamlit as st
except ImportError:
    st = None

# Load environment variables
load_dotenv()

def get_api_key():
    """Retrieve API Key from env or st.secrets"""
    key = os.getenv("GOOGLE_API_KEY")
    if not key and st is not None:
        try:
            key = st.secrets["GOOGLE_API_KEY"]
        except:
            pass
    return key

def get_model(api_key):
    """Returns the configured Gemini model."""
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
    )
    return model

def process_text(text, target_language, improve_mode=False):
    """
    Process the text using Gemini.
    """
    api_key = get_api_key()
    if not api_key:
        return {
            "error": "Chave de API (GOOGLE_API_KEY) não encontrada. Configure nos 'Secrets' do Streamlit Cloud.",
            "detected_language": "Unknown",
            "translated_text": ""
        }

    try:
        model = get_model(api_key)
        
        # Prompt construction
        prompt = f"""
        You are an expert linguist, translator, and copy editor. 
        Your task is to process the following text provided by the user.
    
        Input Text:
        "{text}"
    
        Target Language: {target_language}
    
        Instructions:
        1. Identify the language of the 'Input Text'.
        2. { "If 'Improve Mode' is active: strict instructions to first rewriting the 'Input Text' in its ORIGINAL language to be more fluid, professional, grammatically correct, and easy to read. This is the 'improved_text'. Then, translate this 'improved_text' into the 'Target Language'. " if improve_mode else "Translate the 'Input Text' directly into the 'Target Language'. If 'Improve Mode' is NOT active, 'improved_text' should be null or empty string." }
        3. Return the result in valid JSON format.
    
        Required JSON Structure:
        {{
            "detected_language": "Name of the source language (e.g., Portuguese, English)",
            "improved_text": "The improved version of the original text (only if improve_mode is True, otherwise null)",
            "translated_text": "The final translation in {target_language}"
        }}
        """
        
        response = model.generate_content(prompt)
        # Parse the JSON response
        result = json.loads(response.text)
        
        # Handle cases where the model returns a list
        if isinstance(result, list):
            if len(result) > 0 and isinstance(result[0], dict):
                result = result[0]
            else:
                # Fallback: try to find a dict in the list
                found = False
                for item in result:
                    if isinstance(item, dict):
                        result = item
                        found = True
                        break
                if not found:
                    raise ValueError(f"Unexpected JSON list structure: {result}")
        
        if not isinstance(result, dict):
            raise ValueError(f"Expected dict, got {type(result)}")
            
        return result
    except Exception as e:
        print(f"Error processing text: {e}")
        return {
            "error": str(e),
            "detected_language": "Unknown",
            "improved_text": None,
            "translated_text": "Error during processing."
        }
