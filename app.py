import os
from fastapi import FastAPI, HTTPException, Body, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uvicorn
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

from carbon_footprint_calculator import CarbonFootprintCalculator
from genai_api import GeminiInsightsGenerator
from chroma_db_integration import ChromaDBManager

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY environment variable not set")
    print("Set it using: export GEMINI_API_KEY='your-api-key-here'")
    GEMINI_API_KEY = "your-api-key-here"  # Replace with your actual API key

genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(title="EcoSmart Purchase Advisor API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the ML model
try:
    ml_model = pickle.load(open('cf_classifier_model.pkl', 'rb'))
    print("ML model loaded successfully")
except Exception as e:
    print(f"Error loading ML model: {e}")
    ml_model = None

# Initialize the CF calculator and ChromaDB manager
calculator = CarbonFootprintCalculator()
db_manager = ChromaDBManager(collection_name="products", persistence_path="./chroma_db")

# Initialize the Gemini insights generator
insights_generator = GeminiInsightsGenerator()

# Data models
class ProductInput(BaseModel):
    category_code: str
    brand: str
    price: float
    packaging_material: str
    shipping_mode: str
    usage_duration: str
    repairability_score: int

class RecommendationInput(BaseModel):
    user_id: str
    product_id: str

class PurchaseChoiceInput(BaseModel):
    user_id: str
    product_id: str
    choice: str  # "ai_suggested" or "original"

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to EcoSmart Purchase Advisor API", "status": "active"}

# Calculate CF score for a single product
@app.post("/calculate-cf")
def calculate_cf(product: ProductInput):
    try:
        # Convert input to dictionary
        product_dict = product.dict()
        
        # Calculate CF score
        cf_score = calculator.calculate_cf_score(product_dict)
        cf_category = calculator.classify_cf_score(cf_score)
        
        return {
            "cf_score": round(cf_score, 2),
            "cf_category": cf_category,
            "product": product_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating CF score: {str(e)}")

# Get product alternatives with lower CF scores
@app.get("/alternatives/{product_id}")
def get_alternatives(product_id: str, limit: int = 5):
    try:
        alternatives = db_manager.get_sustainable_alternatives(product_id, limit)
        return {
            "alternatives": alternatives,
            "count": len(alternatives)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding alternatives: {str(e)}")

# Query products by brand
@app.get("/products/brand/{brand}")
def query_by_brand(brand: str, limit: int = 10):
    try:
        products = db_manager.query_by_brand(brand, limit)
        return {
            "products": products,
            "count": len(products)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying products: {str(e)}")

# Query products by CF category
@app.get("/products/category/{category}")
def query_by_cf_category(category: str, limit: int = 10):
    try:
        products = db_manager.query_by_cf_category(category, limit)
        return {
            "products": products,
            "count": len(products)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying products: {str(e)}")

# Get personalized recommendations using Gemini
@app.post("/get-recommendations")
def get_recommendations(input_data: RecommendationInput):
    try:
        user_id = input_data.user_id
        product_id = input_data.product_id
        
        # Get product details
        # This would typically come from the database
        # For now, we'll use a mock product if it's not in the DB
        product = None
        for i, pid in enumerate(db_manager.ids):
            if pid == product_id:
                product = db_manager.products_data[i]
                break
        
        if not product:
            # Mock product for testing
            product = {
                "brand": "apple",
                "category_code": "electronics.smartphone",
                "price": 999.0,
                "packaging_material": "cardboard",
                "shipping_mode": "air",
                "usage_duration": "2 years",
                "repairability_score": 4,
                "cf_score": 75.5,
                "cf_category": "High CF"
            }
        
        # Get alternatives with lower CF
        alternatives = db_manager.get_sustainable_alternatives(product_id, limit=3)
        
        # Generate insights using Gemini
        insights = insights_generator.generate_recommendations(
            user_id=user_id,
            product=product,
            alternatives=alternatives
        )
        
        return {
            "user_id": user_id,
            "product_id": product_id,
            "product_details": product,
            "alternatives": alternatives,
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

# Initialize database from CSV file
@app.post("/admin/init-db")
def initialize_database(file_path: str = Body(..., embed=True)):
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        # Import data into ChromaDB
        db_manager.csv_to_chroma(file_path)
        
        return {
            "status": "success",
            "message": f"Initialized database from {file_path}",
            "record_count": len(db_manager.products_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing database: {str(e)}")

# App startup event
@app.on_event("startup")
async def startup_event():
    # Initialize DB with sample data if available
    if os.path.exists('data.csv'):
        try:
            db_manager.csv_to_chroma('data.csv')
            print(f"Initialized database with {len(db_manager.products_data)} records from data.csv")
        except Exception as e:
            print(f"Error initializing database: {e}")

# Load user purchase history from CSV
def load_user_purchase_history():
    try:
        df = pd.read_csv('df_2.csv')
        return df
    except Exception as e:
        print(f"Error loading user purchase history: {e}")
        return pd.DataFrame()

# Save user purchase history to CSV
def save_user_purchase_history(df):
    try:
        df.to_csv('df_2.csv', index=False)
    except Exception as e:
        print(f"Error saving user purchase history: {e}")

# Get user's sustainable purchase streak
def get_user_streak(user_id: str) -> int:
    df = load_user_purchase_history()
    user_purchases = df[df['user_id'] == user_id].sort_values('date', ascending=False)
    
    streak = 0
    for _, purchase in user_purchases.iterrows():
        if purchase['choice'] == 'ai_suggested':
            streak += 1
        else:
            break
    return streak

# Add this at the top of your file with other imports and global variables
latest_product_data = {}

# Modify your calculate_carbon_footprint endpoint to store the latest product data
@app.post("/calculate-carbon-footprint")
async def calculate_carbon_footprint(input_data: ProductInput):
    try:
        # Your existing carbon footprint calculation code...
        
        # Store the latest product data for use in purchase submission
        global latest_product_data
        latest_product_data = {
            'category_code': input_data.category_code,
            'brand': input_data.brand,
            'price': input_data.price,
            'cf_score': cf_score,  # Make sure this is calculated in your existing code
            'cf_category': cf_category  # Make sure this is calculated in your existing code
        }
        
        return {"carbon_footprint": cf_score, "category": cf_category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Submit purchase choice and handle incentivization
@app.post("/submit-purchase-choice")
async def submit_purchase_choice(input_data: PurchaseChoiceInput):
    try:
        user_id = input_data.user_id
        product_id = input_data.product_id
        choice = input_data.choice
        
        # Get current date
        current_date = pd.Timestamp.now().strftime('%Y-%m-%d')
        
        # Create new purchase record using the latest calculated product data
        new_purchase = {
            'user_id': user_id,
            'product_id': product_id,
            'date': current_date,
            'category_code': latest_product_data.get('category_code', ''),
            'brand': latest_product_data.get('brand', ''),
            'price': latest_product_data.get('price', 0),
            'cf_score': latest_product_data.get('cf_score', 0),
            'cf_category': latest_product_data.get('cf_category', ''),
            'choice': choice
        }
        
        # Load existing data
        try:
            df = pd.read_csv('df_2.csv')
            print(f"Loaded {len(df)} existing records from CSV")
        except Exception as e:
            print(f"Creating new CSV file as existing one couldn't be loaded: {e}")
            df = pd.DataFrame()
        
        # Append new purchase
        df = pd.concat([df, pd.DataFrame([new_purchase])], ignore_index=True)
        
        # Save updated data
        df.to_csv('df_2.csv', index=False)
        print(f"Saved {len(df)} records to CSV file")
        
        # Load and update user streak
        user_streaks = load_user_streaks()
        current_streak = user_streaks.get(user_id, 0)
        
        if choice == 'ai_suggested':
            current_streak += 1
        else:
            current_streak = 0
            
        # Save updated streak
        user_streaks[user_id] = current_streak
        save_user_streaks(user_streaks)
        print(f"Updated streak for user {user_id}: {current_streak}")
        
        # Prepare reward message
        reward_message = ""
        if choice == 'ai_suggested':
            if current_streak == 5:
                reward_message = "Congratulations! You've earned 100 credits for making 5 sustainable purchases in a row!"
            elif current_streak > 5 and current_streak % 5 == 0:
                reward_message = f"Congratulations! You've earned 100 credits for maintaining your streak of {current_streak} sustainable purchases!"
        
        # Update ChromaDB with new purchase
        try:
            db_manager.add_purchase_record(new_purchase)
            print(f"Added purchase record to ChromaDB")
        except Exception as e:
            print(f"Warning: Could not update ChromaDB: {e}")
        
        return {
            "success": True,
            "message": f"Purchase choice recorded successfully. {reward_message}",
            "streak": current_streak
        }
        
    except Exception as e:
        print(f"Error in submit_purchase_choice: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error recording purchase choice: {str(e)}")

# Add an endpoint to get user's current streak
@app.get("/user-streak/{user_id}")
async def get_user_streak(user_id: str):
    try:
        user_streaks = load_user_streaks()
        streak = user_streaks.get(user_id, 0)
        
        # Calculate credits based on streak
        # 100 credits for every 5 sustainable purchases
        credits = (streak // 5) * 100
        
        print(f"Retrieved stats for user {user_id}: streak={streak}, credits={credits}")
        return {
            "success": True,
            "streak": streak,
            "credits": credits
        }
    except Exception as e:
        print(f"Error getting user streak: {e}")
        return {"success": False, "streak": 0, "credits": 0}

def load_user_streaks():
    try:
        if os.path.exists('user_streaks.json'):
            with open('user_streaks.json', 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading user streaks: {e}")
        return {}

def save_user_streaks(streaks):
    try:
        with open('user_streaks.json', 'w') as f:
            json.dump(streaks, f)
    except Exception as e:
        print(f"Error saving user streaks: {e}")

@app.get("/user-streaks-file")
async def get_user_streaks_file():
    try:
        with open('user_streaks.txt', 'r') as f:
            content = f.read()
        return Response(content=content, media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 