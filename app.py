import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uvicorn
import pandas as pd
import numpy as np
import pickle
import json

from carbon_footprint_calculator import CarbonFootprintCalculator
from genai_api import GeminiInsightsGenerator
from chroma_db_integration import ChromaDBManager

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

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 