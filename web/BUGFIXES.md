# Bug Fixes Log

## Issue #1: Pydantic V2 Deprecation Warning

### Problem
```
PydanticDeprecatedSince20: The `dict` method is deprecated; use `model_dump` instead.
```

### Root Cause
The code was using the old Pydantic V1 API method `.dict()` which is deprecated in Pydantic V2.

### Solution
**File:** `app.py` (line 134)

**Before:**
```python
input_data = request.dict()
```

**After:**
```python
input_data = request.model_dump()
```

### Status
✅ **FIXED** - Updated to use Pydantic V2 API

---

## Issue #2: sklearn Feature Names Warning

### Problem
```
UserWarning: X does not have valid feature names, but SimpleImputer was fitted with feature names
```

### Root Cause
The imputer was trained on a pandas DataFrame with feature names, but during prediction, we were passing a numpy array without feature names. This causes sklearn to issue a warning about the mismatch.

### Solution
**File:** `app.py` (lines 137-164)

Changed the data processing pipeline to maintain feature names throughout:

**Before:**
```python
# Build list and convert to numpy array
feature_vector = []
for feature_name in feature_names:
    # ... encoding logic ...
    feature_vector.append(value)

feature_vector = np.array(feature_vector).reshape(1, -1)
feature_vector = imputer.transform(feature_vector)  # ❌ No feature names
feature_vector_scaled = scaler.transform(feature_vector)
```

**After:**
```python
# Build dictionary and convert to DataFrame
feature_dict = {}
for feature_name in feature_names:
    # ... encoding logic ...
    feature_dict[feature_name] = value

# Convert to DataFrame with feature names
feature_df = pd.DataFrame([feature_dict], columns=feature_names)

# Transform with DataFrame (maintains feature names)
feature_df_imputed = pd.DataFrame(
    imputer.transform(feature_df),
    columns=feature_names
)

feature_vector_scaled = scaler.transform(feature_df_imputed)  # ✅ Has feature names
```

### Additional Changes
- **Added import:** `import pandas as pd` to `app.py`
- **Updated:** `requirements.txt` to include `pandas==2.1.3`

### Status
✅ **FIXED** - Now using pandas DataFrame to maintain feature names

---

## Issue #3: Attrition Target Variable in Feature List

### Problem
```
HTTP 500 Error: The feature names should match those that were passed during fit.
Feature names seen at fit time, yet now missing: - Attrition
```

### Root Cause
The `feature_names.pkl` file included "Attrition" (the target variable) in the feature list. When making predictions, we were trying to include "Attrition" as an input feature, but:
1. "Attrition" is the target variable we're trying to predict, not an input
2. The model was trained on features WITHOUT "Attrition"
3. The imputer/scaler expect features without "Attrition"

### Solution
**File:** `app.py` (lines 33-41, 143-170)

**Before:**
```python
feature_names = joblib.load(MODEL_DIR / "feature_names.pkl")
# ... later ...
for feature_name in feature_names:  # ❌ Includes "Attrition"
    value = input_data.get(feature_name)
    # ...
```

**After:**
```python
feature_names_all = joblib.load(MODEL_DIR / "feature_names.pkl")

# Filter out target variable "Attrition" if present
feature_names = [f for f in feature_names_all if f != "Attrition"]

# ... later ...
for feature_name in feature_names:  # ✅ Excludes "Attrition"
    if feature_name not in input_data:
        raise HTTPException(status_code=400, detail=f"Missing required feature: {feature_name}")
    value = input_data[feature_name]
    # ...
```

### Key Changes
1. **Filter on load:** Remove "Attrition" from feature_names when loading
2. **Validation:** Added check to ensure all required features are present
3. **Error handling:** Better error messages for missing features

### Status
✅ **FIXED** - "Attrition" is now properly excluded from input features

---

## Issue #4: Imputer/Scaler Expect "Attrition" Feature Name

### Problem
```
Prediction error: The feature names should match those that were passed during fit.
Feature names seen at fit time, yet now missing: - Attrition
```

### Root Cause
The imputer/scaler were trained on data that included "Attrition" as a column name (even though it wasn't used as a feature). When making predictions, sklearn transformers check that all feature names from training are present. Since we exclude "Attrition" (because we're predicting it), the transformers complain about the missing feature name.

### Solution
**File:** `app.py` (lines 213-271)

**Approach:**
1. Check what features the imputer/scaler expect using `feature_names_in_` attribute
2. If "Attrition" is expected, add it as a dummy column (value 0) to satisfy sklearn's feature name check
3. Pass it through imputer/scaler transformations
4. Remove "Attrition" column before passing to the model (since model was trained without it)

**Key Changes:**
```python
# Check what features imputer expects
if hasattr(imputer, 'feature_names_in_'):
    imputer_features = list(imputer.feature_names_in_)
    
    # Add "Attrition" as dummy column if expected
    if "Attrition" in imputer_features and "Attrition" not in feature_df.columns:
        feature_df["Attrition"] = 0  # Dummy value
    
    # Reorder to match expected order
    feature_df = feature_df[imputer_features]

# Same for scaler
if hasattr(scaler, 'feature_names_in_'):
    scaler_features = list(scaler.feature_names_in_)
    # ... handle similarly
    
# Remove "Attrition" before model prediction
if "Attrition" in feature_df_scaled.columns:
    feature_df_scaled = feature_df_scaled.drop(columns=["Attrition"])
```

### Status
✅ **FIXED** - "Attrition" is handled as dummy column for transformers, then removed before model prediction

---

## Testing

After these fixes, the application should:
1. ✅ No longer show Pydantic deprecation warnings
2. ✅ No longer show sklearn feature names warnings
3. ✅ Continue to work correctly with predictions
4. ✅ Maintain compatibility with the trained model

## How to Apply

The fixes are already applied to the code. If you're running the server, restart it:

```bash
# Stop the current server (Ctrl+C)
# Then restart
cd web
python app.py
```

The warnings should no longer appear when making predictions!

---

**Fixed on:** 2024
**Files Modified:** 
- `web/app.py` (3 changes)
- `web/requirements.txt` (1 change)

**Impact:** 
- Warnings eliminated
- Code updated to modern APIs
- Maintains backward compatibility
- No functional changes to predictions

