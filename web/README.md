# HR Attrition Prediction Web Application

A beautiful web application for predicting employee attrition using a trained Multi-Layer Perceptron (MLP) model.

## Features

- 🎯 Interactive web interface with sliders and selectors
- 📊 Real-time prediction with probability percentage
- 🎨 Modern, responsive design
- 🚀 Fast API backend
- 📈 Visual risk assessment (Low/Medium/High)

## Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- Scikit-learn - Machine Learning model
- Joblib - Model serialization
- Uvicorn - ASGI server

**Frontend:**
- HTML5
- CSS3 (with gradients and animations)
- Vanilla JavaScript
- Responsive design

## Project Structure

```
web/
├── app.py              # FastAPI application
├── static/
│   ├── index.html     # Main HTML page
│   ├── styles.css     # Styling
│   └── script.js      # Frontend logic
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using uv (if in project root):
```bash
uv pip install fastapi uvicorn[standard] pydantic joblib numpy scikit-learn
```

## Running the Application

### Option 1: From web directory
```bash
cd web
python app.py
```

### Option 2: Using uvicorn directly
```bash
cd web
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at: **http://localhost:8000**

## API Endpoints

### `GET /`
- Returns the main HTML interface

### `GET /api/feature-info`
- Returns feature information and ranges for form initialization

### `POST /api/predict`
- Accepts employee data and returns attrition prediction
- **Request Body:** JSON with all employee features
- **Response:** 
  ```json
  {
    "attrition_probability": 75.5,
    "attrition_risk": "High",
    "prediction": "Will Leave"
  }
  ```

### `GET /health`
- Health check endpoint
- Returns server and model status

## Model Information

The application uses a trained MLP model with the following characteristics:
- **Architecture:** 3 hidden layers (100, 50, 25 neurons)
- **Activation:** ReLU
- **Solver:** Adam optimizer
- **Test Accuracy:** 85.8%
- **AUC-ROC:** 0.84

## Input Features

The model requires 30 features grouped into categories:

### Personal Information
- Age, Gender, Marital Status, Distance From Home

### Education
- Education Level, Education Field

### Job Information
- Department, Job Role, Job Level, Business Travel

### Compensation
- Monthly Income, Monthly Rate, Hourly Rate, Daily Rate
- Percent Salary Hike, Stock Option Level

### Work Experience
- Total Working Years, Years At Company
- Years In Current Role, Years Since Last Promotion
- Years With Current Manager, Number of Companies Worked

### Work Environment
- Environment Satisfaction, Job Satisfaction
- Job Involvement, Work Life Balance
- Relationship Satisfaction, Performance Rating
- Training Times Last Year, Over Time

## Screenshots

The application features:
- Clean, modern interface with gradient backgrounds
- Organized form with collapsible sections
- Real-time slider value updates
- Animated prediction results
- Risk level color coding (Green/Yellow/Red)
- Responsive design for mobile and desktop

## Development

To modify the application:

1. **Backend changes:** Edit `app.py`
2. **Frontend HTML:** Edit `static/index.html`
3. **Styling:** Edit `static/styles.css`
4. **JavaScript:** Edit `static/script.js`

The server will auto-reload if using `--reload` flag with uvicorn.

## Troubleshooting

**Model not found:**
- Ensure the `output/` directory exists in the parent directory
- Check that all required .pkl files are present

**Connection refused:**
- Check if port 8000 is available
- Try a different port: `uvicorn app:app --port 8001`

**CORS errors:**
- The app serves static files directly, so CORS shouldn't be an issue
- If using external frontend, add CORS middleware to FastAPI

## License

Part of AITU Programming for AI course project.

