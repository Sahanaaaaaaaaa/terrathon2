from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
from datetime import datetime
from typing import Optional

from carbon_footprint_calculator import CarbonFootprintCalculator
from genai_api import CarbonFootprintGenAI

app = FastAPI(title="Carbon Footprint API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load ML model
try:
    ml_model = joblib.load('cf_classifier_model.pkl')
    print("ML model loaded successfully")
except:
    ml_model = None
    print("ML model not found. Run ml_classifier.py first to generate the model.")

# Initialize CF calculator and GenAI
cf_calculator = CarbonFootprintCalculator()
genai_advisor = CarbonFootprintGenAI()

class ProductInput(BaseModel):
    packaging_material: str
    shipping_mode: str
    usage_duration: str
    repairability_score: int
    category_code: str
    brand: str
    price: float

class UserProductQuery(BaseModel):
    user_id: str
    product_id: str
    brand: str
    purchase_time: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Carbon Footprint API is running (using Gemini AI)"}

@app.post("/calculate-cf")
def calculate_cf(product: ProductInput):
    """Calculate CF score for a product based on its attributes"""
    # Convert to DataFrame for consistent processing
    product_df = pd.DataFrame({
        'packaging_material': [product.packaging_material],
        'shipping_mode': [product.shipping_mode],
        'usage_duration': [product.usage_duration],
        'repairability_score': [product.repairability_score],
        'category_code': [product.category_code],
        'brand': [product.brand],
        'price': [product.price]
    })
    
    # Calculate CF score
    cf_score = cf_calculator.calculate_cf_score(product_df.iloc[0])
    cf_category = cf_calculator.classify_cf_score(cf_score)
    
    return {
        "cf_score": round(cf_score, 2),
        "cf_category": cf_category
    }

@app.post("/predict-cf-category")
def predict_cf_category(product: ProductInput):
    """Predict CF category using ML model"""
    if ml_model is None:
        raise HTTPException(status_code=503, detail="ML model not loaded. Run ml_classifier.py first.")
    
    # Convert to DataFrame for consistent processing
    product_df = pd.DataFrame({
        'packaging_material': [product.packaging_material],
        'shipping_mode': [product.shipping_mode],
        'usage_duration': [product.usage_duration],
        'repairability_score': [product.repairability_score],
        'category_code': [product.category_code],
        'brand': [product.brand],
        'price': [product.price]
    })
    
    # Use ML model to predict
    from ml_classifier import predict_cf_category
    prediction = predict_cf_category(ml_model, product_df)
    
    return {
        "predicted_cf_category": prediction[0]
    }

@app.post("/get-recommendations")
def get_recommendations(query: UserProductQuery):
    """Get personalized recommendations for a user's product purchase using Gemini AI"""
    purchase_time = query.purchase_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get recommendations using GenAI
    recommendations = genai_advisor.generate_recommendations(
        user_id=query.user_id,
        product_id=query.product_id,
        brand=query.brand,
        purchase_time=purchase_time
    )
    
    # Get user's CF score
    user_cf_score, user_cf_category = genai_advisor.get_user_cf_score(query.user_id)
    
    return {
        "user_id": query.user_id,
        "user_cf_score": round(user_cf_score, 2) if user_cf_score else None,
        "user_cf_category": user_cf_category,
        "recommendations": recommendations
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 