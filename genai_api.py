import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Set up Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models to see correct model name
for model in genai.list_models():
    if "gemini" in model.name.lower():
        print(f"Found Gemini model: {model.name}")

class CarbonFootprintGenAI:
    def __init__(self):
        # Load datasets
        self.product_data = pd.read_csv('data_with_cf_scores.csv')
        
        # Create user purchase history dict
        self.user_purchase_history = self.build_user_history()
    
    def build_user_history(self):
        """Build a dictionary of user purchase history"""
        user_history = {}
        
        for _, row in self.product_data.iterrows():
            user_id = row['user_id']
            
            if user_id not in user_history:
                user_history[user_id] = []
            
            user_history[user_id].append({
                'product_id': row['product_id'],
                'category_code': row['category_code'],
                'brand': row['brand'],
                'price': row['price'],
                'cf_score': row['cf_score'],
                'cf_category': row['cf_category']
            })
        
        return user_history
    
    def get_user_cf_score(self, user_id):
        """Calculate average CF score for a user based on purchase history"""
        if user_id not in self.user_purchase_history:
            return None, None
        
        purchases = self.user_purchase_history[user_id]
        if not purchases:
            return None, None
        
        total_cf = sum(item['cf_score'] for item in purchases)
        avg_cf = total_cf / len(purchases)
        
        # Determine user's CF category
        if avg_cf >= 70:
            category = "High CF"
        elif avg_cf >= 40:
            category = "Medium CF"
        else:
            category = "Low CF"
        
        return avg_cf, category
    
    def find_similar_products_with_lower_cf(self, category_code, brand, max_price=None):
        """Find similar products with lower CF scores"""
        # Filter products by category
        category_products = self.product_data[self.product_data['category_code'] == category_code]
        
        # Sort by CF score (ascending)
        sorted_products = category_products.sort_values('cf_score')
        
        # Filter by price if specified
        if max_price is not None:
            sorted_products = sorted_products[sorted_products['price'] <= max_price]
        
        # Get top 3 products with lowest CF
        recommendations = sorted_products.head(3)
        
        return recommendations[['product_id', 'brand', 'price', 'cf_score', 'cf_category']].to_dict('records')
    
    def find_alternative_brands(self, category_code, current_brand):
        """Find alternative brands with lower average CF for the same category"""
        # Filter products by category
        category_products = self.product_data[self.product_data['category_code'] == category_code]
        
        # Group by brand and calculate average CF score
        brand_cf = category_products.groupby('brand')['cf_score'].mean().reset_index()
        
        # Sort by average CF score (ascending)
        sorted_brands = brand_cf.sort_values('cf_score')
        
        # Remove current brand
        alternative_brands = sorted_brands[sorted_brands['brand'] != current_brand]
        
        return alternative_brands.head(3).to_dict('records')
    
    def generate_recommendations(self, user_id, product_id, brand, purchase_time):
        """Generate recommendations using Gemini API based on user data"""
        # Get user's CF score and category
        user_cf_score, user_cf_category = self.get_user_cf_score(user_id)
        
        if not user_cf_score:
            user_cf_score = "Unknown"
            user_cf_category = "Unknown"
        
        # Find the product category
        product_info = self.product_data[self.product_data['product_id'] == product_id]
        if product_info.empty:
            product_category = "Unknown"
        else:
            product_category = product_info.iloc[0]['category_code']
        
        # Find alternative products with lower CF
        alt_products = self.find_similar_products_with_lower_cf(product_category, brand)
        
        # Find alternative brands with lower CF
        alt_brands = self.find_alternative_brands(product_category, brand)
        
        # Generate the prompt for Gemini
        prompt = f"""
        You are a sustainability advisor helping a user make environmentally conscious purchasing decisions.
        
        User Information:
        - User ID: {user_id}
        - Average Carbon Footprint (CF) Score: {user_cf_score}
        - CF Category: {user_cf_category}
        
        Current Product Information:
        - Product ID: {product_id}
        - Brand: {brand}
        - Category: {product_category}
        
        Alternative Products with Lower CF Scores:
        {self._format_alt_products(alt_products)}
        
        Alternative Brands with Lower Average CF in this Category:
        {self._format_alt_brands(alt_brands)}
        
        Please provide the following in your response:
        1. The user's CF score and category based on their purchase history
        2. Which CF category the current product and brand belongs to
        3. Specific recommendations for alternative products or brands that would help reduce the user's carbon footprint
        4. Sustainability tips related to this product category
        """
        
        try:
            # Call Gemini API
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Fallback to local generation if API fails
            print(f"Error using Gemini API: {e}")
            return self._generate_fallback_recommendation(user_id, user_cf_score, user_cf_category, 
                                                        product_id, brand, product_category,
                                                        alt_products, alt_brands)
    
    def _generate_fallback_recommendation(self, user_id, user_cf_score, user_cf_category, 
                                        product_id, brand, product_category,
                                        alt_products, alt_brands):
        """Generate a fallback recommendation if the API fails"""
        alt_product_text = "No alternative products found."
        if alt_products:
            best_alt = alt_products[0]
            alt_product_text = f"Consider {best_alt['brand']} (Product ID: {best_alt['product_id']}) " \
                              f"with a CF score of {best_alt['cf_score']} instead of your current choice."
        
        alt_brand_text = "No alternative brands found."
        if alt_brands:
            best_brand = alt_brands[0]
            alt_brand_text = f"Consider switching to {best_brand['brand']} with a lower average CF score of {best_brand['cf_score']}."
        
        # Generate a simple recommendation
        recommendation = f"""
        ### Carbon Footprint Analysis for User {user_id}
        
        Your CF Score: {user_cf_score}
        Your CF Category: {user_cf_category}
        
        Your selected product ({product_id} by {brand}) falls under the {product_category} category.
        
        ### Recommendations:
        
        {alt_product_text}
        
        {alt_brand_text}
        
        ### Sustainability Tips:
        
        1. Choose products with longer lifespans
        2. Opt for repairable items with high repairability scores
        3. Select products with eco-friendly packaging
        4. Consider local shipping options when available
        5. Recycle your electronics properly when they reach end-of-life
        """
        
        return recommendation
    
    def _format_alt_products(self, alt_products):
        """Format alternative products for the prompt"""
        if not alt_products:
            return "None available"
        
        result = ""
        for i, product in enumerate(alt_products, 1):
            result += f"{i}. Product ID: {product['product_id']}, Brand: {product['brand']}, Price: ${product['price']}, CF Score: {product['cf_score']}, Category: {product['cf_category']}\n"
        
        return result
    
    def _format_alt_brands(self, alt_brands):
        """Format alternative brands for the prompt"""
        if not alt_brands:
            return "None available"
        
        result = ""
        for i, brand in enumerate(alt_brands, 1):
            result += f"{i}. Brand: {brand['brand']}, Average CF Score: {brand['cf_score']}\n"
        
        return result

# Example usage
if __name__ == "__main__":
    advisor = CarbonFootprintGenAI()
    recommendation = advisor.generate_recommendations(
        user_id="u001",
        product_id="p123",
        brand="Dell",
        purchase_time="2022-01-01 10:30:00"
    )
    print(recommendation) 