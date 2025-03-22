import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

def train_cf_classifier():
    # Load data with CF scores
    df = pd.read_csv('data_with_cf_scores.csv')
    
    # Select features and target
    X = df[['packaging_material', 'shipping_mode', 'usage_duration', 'repairability_score', 
           'category_code', 'brand', 'price']]
    y = df['cf_category']  # High CF, Medium CF, Low CF
    
    # Convert 'usage_duration' to numeric (extract years)
    X['usage_duration_years'] = X['usage_duration'].str.extract('(\d+)').astype(int)
    X = X.drop('usage_duration', axis=1)
    
    # Define categorical and numerical features
    categorical_features = ['packaging_material', 'shipping_mode', 'category_code', 'brand']
    numerical_features = ['repairability_score', 'price', 'usage_duration_years']
    
    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # Create and train the model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(report)
    
    # Save the model
    joblib.dump(model, 'cf_classifier_model.pkl')
    
    return model

def predict_cf_category(model, product_data):
    """
    Make predictions for new products
    
    Args:
        model: Trained classifier model
        product_data: DataFrame with product features
    
    Returns:
        Predicted CF category
    """
    # Ensure product_data has the same format as training data
    if 'usage_duration' in product_data.columns:
        product_data['usage_duration_years'] = product_data['usage_duration'].str.extract('(\d+)').astype(int)
        product_data = product_data.drop('usage_duration', axis=1)
    
    # Make prediction
    prediction = model.predict(product_data)
    return prediction

if __name__ == "__main__":
    model = train_cf_classifier()
    
    # Example prediction for a new product
    new_product = pd.DataFrame({
        'packaging_material': ['plastic'],
        'shipping_mode': ['air'],
        'usage_duration': ['2 years'],
        'repairability_score': [3],
        'category_code': ['electronics.smartphone'],
        'brand': ['Samsung'],
        'price': [900]
    })
    
    prediction = predict_cf_category(model, new_product)
    print(f"Predicted CF category for new product: {prediction[0]}") 