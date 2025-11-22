# AgeGroup Feature Implementation

## Overview

Added AgeGroup feature to the HR Attrition Prediction web application. AgeGroup is automatically computed from Age and displayed as a selector in the frontend.

## Changes Made

### 1. Backend (`web/app.py`)

#### Added AgeGroup Calculation Function
```python
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
```

#### Updated PredictionRequest Model
- Added `AgeGroup: Optional[str] = None` to the request model
- AgeGroup is optional because it's computed from Age

#### Automatic AgeGroup Computation
- In the `/api/predict` endpoint, AgeGroup is automatically computed from Age
- Even if the frontend sends a different AgeGroup value, it's overwritten with the computed value
- This ensures consistency between Age and AgeGroup

### 2. Frontend (`web/static/index.html`)

#### Added AgeGroup Selector
- Added a dropdown selector for AgeGroup right after the Age slider
- Options: 18-25, 26-35, 36-45, 46-55, 55+
- Default: 26-35 (matching default Age of 30)
- Includes helper text: "Automatically updated based on Age"

### 3. JavaScript (`web/static/script.js`)

#### Added AgeGroup Calculation Function
```javascript
function calculateAgeGroup(age) {
    if (age <= 25) return "18-25";
    else if (age <= 35) return "26-35";
    else if (age <= 45) return "36-45";
    else if (age <= 55) return "46-55";
    else return "55+";
}
```

#### Auto-Update AgeGroup on Age Change
- When Age slider changes, AgeGroup selector automatically updates
- Uses the same calculation logic as the backend
- Initializes AgeGroup based on default Age value (30 → 26-35)

## Age Group Ranges

| Age Range | AgeGroup Value |
|-----------|---------------|
| 18-25     | "18-25"       |
| 26-35     | "26-35"       |
| 36-45     | "36-45"       |
| 46-55     | "46-55"       |
| 56+       | "55+"         |

## Features

✅ **Automatic Computation**: AgeGroup is computed from Age automatically
✅ **Frontend Display**: AgeGroup selector shows current group
✅ **Real-time Updates**: AgeGroup updates as Age slider moves
✅ **Backend Validation**: Backend ensures AgeGroup matches Age
✅ **Both Features Included**: Both Age and AgeGroup are sent to the model

## User Experience

1. User adjusts Age slider (e.g., to 42)
2. AgeGroup selector automatically updates to "36-45"
3. Both Age (42) and AgeGroup ("36-45") are sent in prediction request
4. Backend verifies and corrects AgeGroup if needed
5. Model receives both features correctly

## Testing

To test:
1. Open the web application
2. Move the Age slider to different values
3. Observe AgeGroup selector updating automatically
4. Submit a prediction - should work without errors
5. Check browser console - no errors expected

## Notes

- AgeGroup is computed client-side for immediate feedback
- Backend also computes it to ensure consistency
- Both Age and AgeGroup are required by the model
- AgeGroup selector can be manually changed, but backend will correct it based on Age

---

**Status**: ✅ **IMPLEMENTED** - AgeGroup feature fully functional

