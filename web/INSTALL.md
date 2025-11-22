# Installation & Setup Guide

## Prerequisites

- Python 3.12 or higher
- All model files in `../output/` directory

## Installation

### Method 1: Using UV (Recommended)

If you're in the project root directory:

```bash
# Sync dependencies (already configured in pyproject.toml)
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate     # On Windows
```

### Method 2: Using pip

From the `web/` directory:

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install fastapi uvicorn[standard] pydantic joblib numpy scikit-learn
```

## Running the Application

### From the web directory:

```bash
cd web
python app.py
```

Or use the start script:

```bash
cd web
./start.sh
```

### Alternative - Using uvicorn directly:

```bash
cd web
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Accessing the Application

Once the server starts, open your browser and navigate to:

**http://localhost:8000**

You should see the HR Attrition Prediction interface.

## Testing the API

### Health Check:
```bash
curl http://localhost:8000/health
```

### Get Feature Info:
```bash
curl http://localhost:8000/api/feature-info
```

### Make a Prediction:
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 35,
    "BusinessTravel": "Travel_Rarely",
    "DailyRate": 800,
    "Department": "Research & Development",
    "DistanceFromHome": 10,
    "Education": 3,
    "EducationField": "Life Sciences",
    "EnvironmentSatisfaction": 3,
    "Gender": "Male",
    "HourlyRate": 65,
    "JobInvolvement": 3,
    "JobLevel": 2,
    "JobRole": "Research Scientist",
    "JobSatisfaction": 3,
    "MaritalStatus": "Married",
    "MonthlyIncome": 5000,
    "MonthlyRate": 14000,
    "NumCompaniesWorked": 2,
    "OverTime": "No",
    "PercentSalaryHike": 15,
    "PerformanceRating": 3,
    "RelationshipSatisfaction": 3,
    "StockOptionLevel": 1,
    "TotalWorkingYears": 10,
    "TrainingTimesLastYear": 3,
    "WorkLifeBalance": 3,
    "YearsAtCompany": 5,
    "YearsInCurrentRole": 3,
    "YearsSinceLastPromotion": 1,
    "YearsWithCurrManager": 3
  }'
```

## Troubleshooting

### Port already in use:
```bash
# Use a different port
python -c "from app import *; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8001)"
```

### Model files not found:
Ensure you've run the notebook and generated the model files in `../output/`:
- mlp_attrition_model.pkl
- scaler.pkl
- imputer.pkl
- label_encoders.pkl
- feature_names.pkl

### Import errors:
Make sure all dependencies are installed:
```bash
uv sync  # or pip install -r requirements.txt
```

## Development Mode

For development with auto-reload:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

This will automatically restart the server when you make changes to the code.

