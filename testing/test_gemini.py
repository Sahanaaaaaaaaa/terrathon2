import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_gemini_api():
    """Test the Gemini API with a simple prompt"""
    # Load environment variables from .env file
    load_dotenv()
    
    # Set up Gemini API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: No API key found. Make sure you set GEMINI_API_KEY in .env file")
        return
    
    genai.configure(api_key=api_key)
    
    # List available models
    print("Available models:")
    models = genai.list_models()
    
    # Find Gemini models
    gemini_models = []
    for model in models:
        if "gemini" in model.name.lower():
            gemini_models.append(model.name)
            print(f"- {model.name}")
    
    if not gemini_models:
        print("No Gemini models found!")
        return
    
    # Choose the first available Gemini model
    model_name = gemini_models[0]
    print(f"\nUsing model: {model_name}")
    
    # Create a model instance
    try:
        model = genai.GenerativeModel(model_name)
        
        # Test with a simple prompt
        prompt = "Generate 3 sustainability tips for electronics consumers."
        print(f"\nSending prompt: {prompt}")
        
        response = model.generate_content(prompt)
        print("\nResponse:")
        print(response.text)
        
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nError testing Gemini API: {e}")
        print("\nFallback to local generation:")
        print("""
        Sustainability Tips for Electronics Consumers:
        
        1. Extend device lifespan: Keep your electronics longer by maintaining them properly, installing updates, and repairing rather than replacing when possible.
        
        2. Choose energy-efficient products: Look for ENERGY STAR certified devices that consume less electricity and reduce your carbon footprint.
        
        3. Recycle properly: When it's time to replace, ensure your old devices are recycled through certified e-waste programs to recover valuable materials and prevent toxic substances from entering landfills.
        """)

if __name__ == "__main__":
    test_gemini_api() 