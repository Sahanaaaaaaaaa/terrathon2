# EcoSmart Purchase Advisor

A sustainability-focused hackathon project that calculates the carbon footprint of products and provides personalized recommendations for more sustainable shopping choices.

## Features

- Carbon footprint calculation for various product categories
- Personalized recommendations using Google's Gemini AI
- Brand sustainability rankings
- Interactive web UI for easy access
- Processing of both small and large datasets

## Technology Stack

- Backend: Python with FastAPI
- Frontend: HTML, CSS, JavaScript with Bootstrap
- AI: Google Gemini API for insights generation
- Data Analysis: Pandas and NumPy

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the API server: `python main.py`
4. Open `frontend/index.html` in your browser

## Data Processing

The project includes two main datasets:
- `data.csv`: A small dataset with pre-defined sustainability metrics
- `df_2.csv`: A larger dataset where sustainability metrics are generated

To process the larger dataset, run:
```
python process_df2.py
```

## Architecture

- `data.csv` - Sample dataset with added sustainability columns
- `carbon_footprint_calculator.py` - Core logic for CF calculation
- `ml_classifier.py` - Machine learning model for CF classification
- `genai_api.py` - Gemini AI integration for personalized recommendations
- `app.py` - FastAPI backend server
- `frontend/index.html` - Simple web interface

## Input Format

The frontend expects:
- UserID
- Product
- Brand
- Time of Purchase

## Output

The Gemini AI API provides:
- User's CF score from purchase history
- User's CF category
- Product and brand CF category
- Recommendations for alternative products/brands with lower CF

## Future Enhancements

- Integration with e-commerce platforms
- Mobile app for real-time CF calculation while shopping
- Expanded dataset with more product categories
- Carbon offset suggestions
- Community features for comparing and tracking CF improvements 