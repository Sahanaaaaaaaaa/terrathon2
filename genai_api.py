import os
import json
import random
from typing import Dict, List, Any, Optional

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google.generativeai module not available. Install with: pip install google-generativeai")

# Set up Google Gemini API key
# Get your API key from https://ai.google.dev/
api_key = os.environ.get('GEMINI_API_KEY', '')
if not api_key:
    print("WARNING: GEMINI_API_KEY environment variable not set")
    print("Set it using: export GEMINI_API_KEY='your-api-key-here'")

# Configure the Gemini API
if api_key and GENAI_AVAILABLE:
    genai.configure(api_key=api_key)
    # List available models
    try:
        for m in genai.list_models():
            if 'gemini' in m.name:
                print(f"Found Gemini model: {m.name}")
    except Exception as e:
        print(f"Error listing Gemini models: {e}")

class GeminiInsightsGenerator:
    """Class to generate personalized sustainability insights using Google's Gemini API"""
    
    def __init__(self, model_name="gemini-1.5-flash"):
        """Initialize the Gemini insights generator with a specific model"""
        self.model_name = model_name
        self.api_key = api_key
        self.genai_available = GENAI_AVAILABLE
        
        # Mock data for user - in a real application, this would come from a database
        self.mock_user_data = {
            "user123": {
                "purchase_history": [
                    {"brand": "apple", "product": "iphone", "cf_score": 75},
                    {"brand": "samsung", "product": "tv", "cf_score": 65},
                    {"brand": "dell", "product": "laptop", "cf_score": 60}
                ],
                "cf_score": 68,
                "cf_category": "Medium CF",
                "preferences": ["electronics", "gadgets", "home appliances"]
            },
            "user456": {
                "purchase_history": [
                    {"brand": "bosch", "product": "refrigerator", "cf_score": 45},
                    {"brand": "dell", "product": "monitor", "cf_score": 40},
                    {"brand": "bequiet", "product": "power supply", "cf_score": 30}
                ],
                "cf_score": 38,
                "cf_category": "Low CF",
                "preferences": ["electronics", "sustainable brands"]
            }
        }
    
    def get_model(self):
        """Get the Gemini model"""
        if not self.api_key or not self.genai_available:
            return None
        
        try:
            # For text-only input
            return genai.GenerativeModel(self.model_name)
        except Exception as e:
            print(f"Error loading Gemini model: {e}")
            return None
    
    def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """Get user data - mock implementation"""
        # In a real application, this would query a user database
        return self.mock_user_data.get(user_id, {
            "purchase_history": [],
            "cf_score": 50,  # Default CF score
            "cf_category": "Medium CF",
            "preferences": []
        })
    
    def generate_prompt(self, user_id: str, product: Dict[str, Any], alternatives: List[Dict[str, Any]]) -> str:
        """Generate a prompt for Gemini based on user and product data"""
        user_data = self.get_user_data(user_id)
        
        # Format the product data
        product_str = f"""
Product: {product.get('category_code', 'Unknown category')}
Brand: {product.get('brand', 'Unknown brand')}
Price: ${product.get('price', 0):.2f}
Carbon Footprint Score: {product.get('cf_score', 'N/A')}
Carbon Footprint Category: {product.get('cf_category', 'Unknown')}
Packaging: {product.get('packaging_material', 'Unknown')}
Shipping: {product.get('shipping_mode', 'Unknown')}
Expected Usage: {product.get('usage_duration', 'Unknown')}
Repairability: {product.get('repairability_score', 'Unknown')}/10
"""

        # Format alternatives
        alternatives_str = ""
        for i, alt in enumerate(alternatives, 1):
            alternatives_str += f"""
Alternative {i}:
- Brand: {alt.get('brand', 'Unknown brand')}
- Product: {alt.get('category_code', 'Unknown category')}
- Price: ${alt.get('price', 0):.2f}
- CF Score: {alt.get('cf_score', 'N/A')}
- CF Category: {alt.get('cf_category', 'Unknown')}
"""

        # Format user's purchase history
        history_str = ""
        for i, purchase in enumerate(user_data.get('purchase_history', []), 1):
            history_str += f"- {purchase.get('brand', 'Unknown brand')} {purchase.get('product', 'product')} (CF: {purchase.get('cf_score', 'N/A')})\n"
        
        prompt = f"""
You are an expert sustainability advisor helping users make eco-friendly purchasing decisions.

USER INFORMATION:
User ID: {user_id}
Overall Carbon Footprint: {user_data.get('cf_score', 'N/A')} ({user_data.get('cf_category', 'Unknown')})
Purchase History:
{history_str if history_str else "No purchase history available"}

CURRENT PRODUCT:
{product_str}

ALTERNATIVE PRODUCTS WITH LOWER CARBON FOOTPRINT:
{alternatives_str if alternatives_str else "No alternatives available"}

Based on this information, please provide the following insights:
1. An assessment of the carbon footprint of the current product
2. How this purchase would impact the user's overall sustainability score
3. Specific recommendations for more sustainable alternatives
4. Practical sustainability tips related to this product category
5. Information about the brand's sustainability practices

Format your response as JSON with the following keys: 
"product_assessment", "user_impact", "alternatives_recommendation", "sustainability_tips", "brand_info"

Keep your response focused and concise, with each section around 2-3 sentences.
"""
        return prompt
    
    def generate_recommendations(self, user_id: str, product: Dict[str, Any], alternatives: List[Dict[str, Any]] = None) -> Dict[str, str]:
        """Generate sustainability recommendations for a user's product"""
        if alternatives is None:
            alternatives = []
            
        model = self.get_model()
        
        if not model:
            # Return mock data if model isn't available
            return {
                "product_assessment": "This product has a high carbon footprint score, indicating significant environmental impact.",
                "user_impact": "This purchase would increase your overall carbon footprint.",
                "alternatives_recommendation": "Consider more sustainable alternatives from brands with better environmental practices.",
                "sustainability_tips": "Extend the product's lifespan through proper maintenance. Recycle responsibly at end-of-life.",
                "brand_info": "This brand has moderate sustainability practices compared to industry standards."
            }
        
        # Generate the prompt
        prompt = self.generate_prompt(user_id, product, alternatives)
        
        try:
            # Generate response from Gemini
            response = model.generate_content(prompt)
            
            # Parse the response - expecting JSON format
            try:
                # Try to extract JSON from the response
                response_text = response.text
                
                # Sometimes Gemini adds ```json and ``` around the response
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].strip()
                
                insights = json.loads(response_text)
                return insights
            except json.JSONDecodeError:
                # Fallback to text parsing if JSON extraction fails
                print("Warning: Failed to parse JSON from Gemini response")
                response_text = response.text
                
                # Create a structured response
                return {
                    "product_assessment": "Unable to parse structured response from AI model.",
                    "user_impact": "Please check your API configuration.",
                    "alternatives_recommendation": response_text[:100] + "...",
                    "sustainability_tips": "Try again later.",
                    "brand_info": "Service temporarily unavailable in structured format."
                }
                
        except Exception as e:
            print(f"Error generating Gemini insights: {e}")
            return {
                "product_assessment": f"Error: {str(e)}",
                "user_impact": "Could not generate insights due to an error.",
                "alternatives_recommendation": "Please try again later.",
                "sustainability_tips": "Service temporarily unavailable.",
                "brand_info": "Could not retrieve brand information."
            }

# Example usage
if __name__ == "__main__":
    advisor = GeminiInsightsGenerator()
    recommendation = advisor.generate_recommendations(
        user_id="u001",
        product={
            "category_code": "electronics",
            "brand": "Dell",
            "price": 1000,
            "cf_score": 60,
            "cf_category": "Medium CF"
        },
        alternatives=[
            {
                "category_code": "electronics",
                "brand": "Apple",
                "price": 1200,
                "cf_score": 75,
                "cf_category": "High CF"
            },
            {
                "category_code": "electronics",
                "brand": "Samsung",
                "price": 900,
                "cf_score": 65,
                "cf_category": "Medium CF"
            }
        ]
    )
    print(recommendation) 