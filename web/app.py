"""
FastAPI Application for HR Attrition Prediction
Serves a web interface to predict employee attrition using trained MLP model
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(title="HR Attrition Prediction", version="1.0")

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "output"
STATIC_DIR = Path(__file__).resolve().parent / "static"

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Load model and artifacts
print("Loading model and artifacts...")
try:
    mlp_model = joblib.load(MODEL_DIR / "mlp_attrition_model.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    imputer = joblib.load(MODEL_DIR / "imputer.pkl")
    label_encoders = joblib.load(MODEL_DIR / "label_encoders.pkl")
    feature_names_all = joblib.load(MODEL_DIR / "feature_names.pkl")
    
    # Filter out target variable "Attrition" if present
    feature_names = [f for f in feature_names_all if f != "Attrition"]
    
    print("✓ Model loaded successfully!")
    print(f"✓ Number of features: {len(feature_names)}")
    if "Attrition" in feature_names_all:
        print("⚠️  Removed 'Attrition' from feature list (it's the target variable)")
except Exception as e:
    print(f"Error loading model: {e}")
    raise

# Define request model
class PredictionRequest(BaseModel):
    Age: int
    AgeGroup: Optional[str] = None  # Will be computed from Age if not provided
    BusinessTravel: str
    DailyRate: int
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    HourlyRate: int
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: int
    SalarySlab: Optional[str] = None  # Will be computed from MonthlyIncome if not provided
    MonthlyRate: int
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int

# Define response model
class PredictionResponse(BaseModel):
    attrition_probability: float
    attrition_risk: str
    prediction: str

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page"""
    html_file = Path(__file__).parent / "static" / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    return HTMLResponse(content="<h1>Welcome to HR Attrition Prediction API</h1>")

@app.get("/api/feature-info")
async def get_feature_info():
    """Get feature information for the frontend"""
    feature_info = {
        "BusinessTravel": ["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
        "Department": ["Human Resources", "Research & Development", "Sales"],
        "EducationField": ["Human Resources", "Life Sciences", "Marketing", "Medical", "Other", "Technical Degree"],
        "Gender": ["Female", "Male"],
        "JobRole": [
            "Healthcare Representative", "Human Resources", "Laboratory Technician",
            "Manager", "Manufacturing Director", "Research Director",
            "Research Scientist", "Sales Executive", "Sales Representative"
        ],
        "MaritalStatus": ["Divorced", "Married", "Single"],
        "OverTime": ["No", "Yes"],
        "ranges": {
            "Age": {"min": 18, "max": 65, "default": 30},
            "DailyRate": {"min": 100, "max": 1500, "default": 800},
            "DistanceFromHome": {"min": 1, "max": 30, "default": 10},
            "Education": {"min": 1, "max": 5, "default": 3},
            "EnvironmentSatisfaction": {"min": 1, "max": 4, "default": 3},
            "HourlyRate": {"min": 30, "max": 100, "default": 65},
            "JobInvolvement": {"min": 1, "max": 4, "default": 3},
            "JobLevel": {"min": 1, "max": 5, "default": 2},
            "JobSatisfaction": {"min": 1, "max": 4, "default": 3},
            "MonthlyIncome": {"min": 1000, "max": 20000, "default": 5000},
            "MonthlyRate": {"min": 2000, "max": 27000, "default": 14000},
            "NumCompaniesWorked": {"min": 0, "max": 10, "default": 2},
            "PercentSalaryHike": {"min": 11, "max": 25, "default": 15},
            "PerformanceRating": {"min": 3, "max": 4, "default": 3},
            "RelationshipSatisfaction": {"min": 1, "max": 4, "default": 3},
            "StockOptionLevel": {"min": 0, "max": 3, "default": 1},
            "TotalWorkingYears": {"min": 0, "max": 40, "default": 10},
            "TrainingTimesLastYear": {"min": 0, "max": 6, "default": 3},
            "WorkLifeBalance": {"min": 1, "max": 4, "default": 3},
            "YearsAtCompany": {"min": 0, "max": 40, "default": 5},
            "YearsInCurrentRole": {"min": 0, "max": 20, "default": 3},
            "YearsSinceLastPromotion": {"min": 0, "max": 15, "default": 1},
            "YearsWithCurrManager": {"min": 0, "max": 20, "default": 3}
        }
    }
    return feature_info

def calculate_age_group(age: int) -> str:
    """Calculate age group from age"""
    if age <= 25:
        return "18-25"
    elif age <= 35:
        return "26-35"
    elif age <= 45:
        return "36-45"
    elif age <= 55:
        return "46-55"
    else:
        return "55+"

def calculate_salary_slab(monthly_income: int) -> str:
    """Calculate salary slab from monthly income"""
    if monthly_income <= 5000:
        return "Upto 5k"
    elif monthly_income <= 10000:
        return "5k-10k"
    elif monthly_income <= 15000:
        return "10k-15k"
    else:
        return "15k+"

@app.post("/api/predict", response_model=PredictionResponse)
async def predict_attrition(request: PredictionRequest):
    """Predict employee attrition probability"""
    try:
        # Convert request to dictionary
        input_data = request.model_dump()
        
        # Compute AgeGroup from Age if not provided or if it doesn't match
        age = input_data.get("Age")
        if age is not None:
            computed_age_group = calculate_age_group(age)
            # Update AgeGroup to match computed value
            input_data["AgeGroup"] = computed_age_group
        
        # Compute SalarySlab from MonthlyIncome if not provided or if it doesn't match
        monthly_income = input_data.get("MonthlyIncome")
        if monthly_income is not None:
            computed_salary_slab = calculate_salary_slab(monthly_income)
            # Update SalarySlab to match computed value
            input_data["SalarySlab"] = computed_salary_slab
        
        # Prepare feature vector in the correct order
        # feature_names already excludes "Attrition" (filtered during load)
        feature_dict = {}
        for feature_name in feature_names:
            # Get value from input data
            if feature_name not in input_data:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Missing required feature: {feature_name}"
                )
            
            value = input_data[feature_name]
            
            # Encode categorical variables
            if feature_name in label_encoders:
                try:
                    # Convert value to string for encoding
                    value = str(value)
                    value = label_encoders[feature_name].transform([value])[0]
                except ValueError:
                    # If value not in encoder, use the first class
                    value = 0
            
            feature_dict[feature_name] = value
        
        # Convert to DataFrame to maintain feature names
        # feature_names is already filtered (no "Attrition")
        feature_df = pd.DataFrame([feature_dict], columns=feature_names)
        
        # Check what features the imputer expects
        # sklearn transformers have feature_names_in_ attribute
        imputer_features = None
        if hasattr(imputer, 'feature_names_in_'):
            imputer_features = list(imputer.feature_names_in_)
        
        # Ensure DataFrame has the exact columns the imputer expects
        if imputer_features:
            # Add any missing columns that imputer expects
            # If "Attrition" is expected, add it as a dummy column (we're predicting it, not using it)
            for col in imputer_features:
                if col not in feature_df.columns:
                    if col == "Attrition":
                        feature_df[col] = 0  # Dummy value for Attrition (won't affect prediction)
                    else:
                        feature_df[col] = 0  # Fill other missing columns with 0
            
            # Reorder columns to match imputer's expected order
            feature_df = feature_df[imputer_features]
        
        # Impute missing values (if any)
        feature_df_imputed = pd.DataFrame(
            imputer.transform(feature_df),
            columns=feature_df.columns
        )
        
        # Check what features the scaler expects
        scaler_features = None
        if hasattr(scaler, 'feature_names_in_'):
            scaler_features = list(scaler.feature_names_in_)
        
        # Ensure DataFrame has the exact columns the scaler expects
        if scaler_features:
            # Add any missing columns that scaler expects
            # If "Attrition" is expected, ensure it's present (with dummy value)
            for col in scaler_features:
                if col not in feature_df_imputed.columns:
                    if col == "Attrition":
                        feature_df_imputed[col] = 0  # Dummy value for Attrition
                    else:
                        feature_df_imputed[col] = 0
            
            # Reorder columns to match scaler's expected order
            feature_df_imputed = feature_df_imputed[scaler_features]
        
        # Remove "Attrition" before scaling if present (we're predicting it, not using it as input)
        # But first, let's check if scaler expects it - if so, we'll keep it for the scaler transform
        # then remove it before model prediction
        has_attrition = "Attrition" in feature_df_imputed.columns
        
        # Scale features
        feature_vector_scaled = scaler.transform(feature_df_imputed)
        
        # Convert back to DataFrame and remove "Attrition" if present before model prediction
        if has_attrition and scaler_features:
            feature_df_scaled = pd.DataFrame(feature_vector_scaled, columns=scaler_features)
            # Remove Attrition column before passing to model
            feature_df_scaled = feature_df_scaled.drop(columns=["Attrition"], errors='ignore')
            feature_vector_scaled = feature_df_scaled.values
        
        # Make prediction
        prediction_proba = mlp_model.predict_proba(feature_vector_scaled)[0]
        attrition_probability = float(prediction_proba[1])  # Probability of attrition
        prediction = int(mlp_model.predict(feature_vector_scaled)[0])
        
        # Determine risk level
        if attrition_probability < 0.3:
            risk = "Low"
        elif attrition_probability < 0.6:
            risk = "Medium"
        else:
            risk = "High"
        
        return PredictionResponse(
            attrition_probability=attrition_probability * 100,  # Convert to percentage
            attrition_risk=risk,
            prediction="Will Leave" if prediction == 1 else "Will Stay"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}") from e

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": mlp_model is not None}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("Starting HR Attrition Prediction Server")
    print("="*60)
    print(f"Model: {MODEL_DIR / 'mlp_attrition_model.pkl'}")
    print(f"Features: {len(feature_names)}")
    print("\nServer will be available at: http://localhost:8000")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)

