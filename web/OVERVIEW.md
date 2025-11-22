# 🎯 HR Attrition Prediction Web Application - Overview

## 📋 Summary

A complete web application for predicting employee attrition probability using a trained Multi-Layer Perceptron (MLP) neural network. The app features an intuitive interface with interactive sliders and dropdowns for all 30 employee features.

## ✨ Features

### Frontend (HTML/CSS/JavaScript)
- **Interactive Input Controls:**
  - 23 range sliders with real-time value display
  - 7 dropdown selectors for categorical features
  - Organized into 6 logical sections
  
- **Visual Design:**
  - Modern gradient UI (purple/blue theme)
  - Responsive layout (desktop & mobile)
  - Smooth animations and transitions
  - Real-time slider value updates
  
- **Results Display:**
  - Attrition probability percentage (0-100%)
  - Visual progress bar with color gradient
  - Risk level badge (Low/Medium/High)
  - Clear prediction outcome (Will Stay / Will Leave)
  - Color-coded results (green = safe, yellow = caution, red = risk)

### Backend (FastAPI)
- **Model Integration:**
  - Loads pre-trained MLP model from `../output/`
  - Handles feature encoding and scaling
  - Performs missing value imputation
  
- **API Endpoints:**
  - `GET /` - Serves main HTML interface
  - `GET /api/feature-info` - Returns feature metadata
  - `POST /api/predict` - Processes prediction requests
  - `GET /health` - Health check endpoint
  
- **Error Handling:**
  - Validates input data
  - Handles missing or invalid features
  - Returns informative error messages

## 📁 File Structure

```
web/
├── app.py                 # FastAPI backend (200+ lines)
├── static/
│   ├── index.html        # Main interface (300+ lines)
│   ├── styles.css        # Styling (400+ lines)
│   └── script.js         # Frontend logic (150+ lines)
├── requirements.txt       # Python dependencies
├── start.sh              # Quick start script
├── README.md             # User documentation
├── INSTALL.md            # Installation guide
└── OVERVIEW.md           # This file
```

## 🎨 UI Sections

### 1. Personal Information (4 fields)
- Age (18-65)
- Gender (Male/Female)
- Marital Status (Single/Married/Divorced)
- Distance From Home (1-30 km)

### 2. Education (2 fields)
- Education Level (1-5)
- Education Field (6 options)

### 3. Job Information (4 fields)
- Department (3 options)
- Job Role (9 options)
- Job Level (1-5)
- Business Travel (3 options)

### 4. Compensation (6 fields)
- Monthly Income ($1k-$20k)
- Monthly Rate ($2k-$27k)
- Hourly Rate ($30-$100)
- Daily Rate ($100-$1500)
- Percent Salary Hike (11-25%)
- Stock Option Level (0-3)

### 5. Work Experience (6 fields)
- Total Working Years (0-40)
- Years At Company (0-40)
- Years In Current Role (0-20)
- Years Since Last Promotion (0-15)
- Years With Current Manager (0-20)
- Number of Companies Worked (0-10)

### 6. Work Environment (8 fields)
- Environment Satisfaction (1-4)
- Job Satisfaction (1-4)
- Job Involvement (1-4)
- Work Life Balance (1-4)
- Relationship Satisfaction (1-4)
- Performance Rating (3-4)
- Training Times Last Year (0-6)
- Over Time (Yes/No)

## 🚀 Quick Start

```bash
# 1. Ensure model files exist
ls ../output/*.pkl

# 2. Install dependencies (if not already done)
uv sync  # or: pip install -r requirements.txt

# 3. Run the application
python app.py

# 4. Open browser
# Navigate to: http://localhost:8000
```

## 📊 Model Information

- **Architecture:** MLP with 3 hidden layers (100, 50, 25 neurons)
- **Training Accuracy:** 94.8%
- **Test Accuracy:** 85.8%
- **AUC-ROC Score:** 0.84
- **F1-Score:** 0.46
- **Training Time:** 35 iterations

## 🎯 Usage Flow

1. **User opens the web interface** at `http://localhost:8000`
2. **Adjusts sliders and selectors** to input employee data
3. **Clicks "Predict Attrition Risk"** button
4. **JavaScript collects form data** and sends POST request to `/api/predict`
5. **Backend processes data:**
   - Encodes categorical variables
   - Imputes any missing values
   - Scales features
   - Makes prediction with MLP model
6. **Returns JSON response** with probability, risk level, and prediction
7. **Frontend displays results** with animated visualization

## 🔧 Technical Details

### Request Format
```json
{
  "Age": 35,
  "Gender": "Male",
  "MaritalStatus": "Married",
  "Education": 3,
  "Department": "Research & Development",
  "JobRole": "Research Scientist",
  "MonthlyIncome": 5000,
  ...
}
```

### Response Format
```json
{
  "attrition_probability": 25.5,
  "attrition_risk": "Low",
  "prediction": "Will Stay"
}
```

### Risk Level Calculation
- **Low:** < 30% probability (green)
- **Medium:** 30-60% probability (yellow)
- **High:** > 60% probability (red)

## 🎨 Design Highlights

- **Color Scheme:** Purple-blue gradient primary, semantic colors for results
- **Typography:** Segoe UI font family
- **Layout:** CSS Grid for responsive design
- **Animations:** Smooth transitions, fade-in effects, progress bar animation
- **Accessibility:** Clear labels, sufficient contrast, keyboard navigation

## 🔒 Security & Validation

- Input validation on both frontend and backend
- Type checking with Pydantic models
- Error handling for invalid/missing values
- Safe model loading with try-except blocks

## 📈 Future Enhancements

Potential improvements:
- Add feature importance visualization
- Include confidence intervals
- Batch prediction support
- Export prediction reports
- Historical prediction tracking
- User authentication
- Docker containerization

## 📝 Notes

- The application requires all model artifacts in `../output/`
- Runs on port 8000 by default (configurable)
- Designed for local deployment
- No database required
- Stateless API design

## 🏆 Achievement

✅ Complete end-to-end ML web application
✅ Professional UI/UX design
✅ RESTful API with FastAPI
✅ Real-time predictions
✅ Comprehensive documentation
✅ Production-ready code structure

---

**Built with:** Python, FastAPI, scikit-learn, HTML5, CSS3, JavaScript
**Course:** AITU Programming for AI
**Project:** Employee Attrition Prediction System

