# EcoSmart Purchase Advisor

A sustainability-focused project that calculates the carbon footprint of products and provides personalized recommendations for more eco-friendly shopping choices.

## Features

- Carbon footprint calculation for various product categories
- Category-based eco-friendly product recommendations
- Interactive shopping interface with environmental impact analysis
- Browser extension-like experience for analyzing cart sustainability
- User sustainability streak tracking and rewards
- Real-time product swapping with eco-friendly alternatives
- Image handling with graceful fallbacks

## Technology Stack

- Frontend: HTML, CSS, JavaScript with Bootstrap 5
- Backend: Python with FastAPI
- AI: Google Gemini API for insights generation
- Data Analysis: Pandas and NumPy
- Vector Database: ChromaDB for product similarity search

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the API server: `python main.py`
4. Open `frontend/shop.html` in your browser

## How It Works

### Shopping Interface
The shopping interface allows users to:
- Browse products with clear sustainability information
- Add products to cart
- View the environmental impact of their cart
- Get eco-friendly product recommendations from the same category
- Swap to eco-friendly alternatives with a single click

### Environmental Impact Analysis
- Each product has a Carbon Footprint (CF) score
- The system analyzes the cart to find items with high CF scores
- Category-based alternatives with lower CF scores are suggested
- Swapping to eco-friendly alternatives increases the user's sustainability streak

### Browser Extension Experience
The interface simulates a browser extension that:
- Analyzes the user's cart automatically
- Provides a summary of the environmental impact
- Offers detailed analysis with recommendations
- Shows sustainability tips

## Architecture

- `data.csv` - Sample dataset with added sustainability columns
- `carbon_footprint_calculator.py` - Core logic for CF calculation
- `ml_classifier.py` - Machine learning model for CF classification
- `genai_api.py` - Gemini AI integration for personalized recommendations
- `app.py` - FastAPI backend server
- `frontend/shop.html` - Interactive shopping interface

## Data Processing Flow

1. Product data is loaded with carbon footprint scores
2. Machine learning model (Random Forest) helps classify items
3. User cart items are analyzed for their environmental impact
4. ChromaDB finds similar but more eco-friendly alternatives
5. Gemini AI helps generate natural language recommendations
6. Results are displayed in an interactive interface

## Future Enhancements

- Integration with e-commerce platforms
- Mobile app for real-time CF calculation while shopping
- Expanded dataset with more product categories
- Carbon offset suggestions
- Community features for comparing and tracking CF improvements
- Full-featured browser extension implementation 