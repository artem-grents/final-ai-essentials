# 🚀 Quick Start Guide - Web Application

## What Was Created

A complete **HR Attrition Prediction Web Application** in the `./web/` directory with:

- ✅ **FastAPI Backend** (`app.py`) - Serves the model and API
- ✅ **Beautiful HTML Interface** (`static/index.html`) - User-friendly form
- ✅ **Modern CSS Styling** (`static/styles.css`) - Purple gradient theme
- ✅ **Interactive JavaScript** (`static/script.js`) - Real-time predictions
- ✅ **Complete Documentation** - README, INSTALL, OVERVIEW guides

## 🎯 Features

- **30 Input Features** via sliders and dropdowns
- **Real-time Predictions** with probability percentage
- **Visual Results** with color-coded risk levels
- **Responsive Design** works on desktop and mobile
- **Model Integration** uses your trained MLP from `./output/`

## 🏃 How to Run (3 Steps)

### Step 1: Install Dependencies (if needed)

From project root:
```bash
uv sync
```

Or from web directory:
```bash
cd web
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
cd web
python app.py
```

Or use the start script:
```bash
cd web
./start.sh
```

### Step 3: Open Browser

Navigate to: **http://localhost:8000**

## 🎨 What You'll See

1. **Header** - Beautiful purple gradient with title
2. **Form Section** - Organized input fields in 6 categories:
   - 📋 Personal Information
   - 🎓 Education
   - 💼 Job Information
   - 💰 Compensation
   - ⏱️ Work Experience
   - 🏢 Work Environment
3. **Results Panel** - Shows:
   - Attrition probability (as percentage)
   - Visual progress bar
   - Risk level (Low/Medium/High)
   - Prediction (Will Stay / Will Leave)

## 📊 Example Usage

1. Adjust the sliders (Age, Income, etc.)
2. Select from dropdowns (Department, Job Role, etc.)
3. Click **"Predict Attrition Risk"** button
4. View results in the right panel

## 🔗 API Endpoints

- `GET /` - Main interface
- `POST /api/predict` - Make predictions
- `GET /api/feature-info` - Get feature metadata
- `GET /health` - Check server status

## 📝 Files Created

```
web/
├── app.py              # FastAPI server (214 lines)
├── static/
│   ├── index.html     # UI interface (340 lines)
│   ├── styles.css     # Styling (415 lines)
│   └── script.js      # Frontend logic (157 lines)
├── requirements.txt    # Dependencies
├── start.sh           # Start script
├── README.md          # Full documentation
├── INSTALL.md         # Installation guide
└── OVERVIEW.md        # Technical overview
```

## ✅ Model Information

Your trained MLP model:
- **Test Accuracy:** 85.8%
- **AUC-ROC:** 0.84
- **Architecture:** 3 layers (100, 50, 25 neurons)

## 🐛 Troubleshooting

**Port 8000 already in use?**
```bash
python -c "from app import *; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8001)"
```

**Model not found?**
Ensure you ran the notebook and have files in `./output/`:
- mlp_attrition_model.pkl
- scaler.pkl
- imputer.pkl
- label_encoders.pkl
- feature_names.pkl

**Import errors?**
Install dependencies: `uv sync` or `pip install -r web/requirements.txt`

## 🎉 That's It!

Your web application is ready to use. Enjoy predicting employee attrition with a beautiful, interactive interface!

---

**Need Help?** Check the detailed guides:
- `web/README.md` - Complete documentation
- `web/INSTALL.md` - Installation instructions
- `web/OVERVIEW.md` - Technical details

