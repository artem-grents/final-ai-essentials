// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeSliders();
    initializeForm();
});

// Calculate age group from age
function calculateAgeGroup(age) {
    if (age <= 25) {
        return "18-25";
    } else if (age <= 35) {
        return "26-35";
    } else if (age <= 45) {
        return "36-45";
    } else if (age <= 55) {
        return "46-55";
    } else {
        return "55+";
    }
}

// Calculate salary slab from monthly income
function calculateSalarySlab(monthlyIncome) {
    if (monthlyIncome <= 5000) {
        return "Upto 5k";
    } else if (monthlyIncome <= 10000) {
        return "5k-10k";
    } else if (monthlyIncome <= 15000) {
        return "10k-15k";
    } else {
        return "15k+";
    }
}

// Initialize all sliders to update their displayed values
function initializeSliders() {
    const sliders = document.querySelectorAll('.slider');
    
    sliders.forEach(slider => {
        const valueDisplay = document.getElementById(`${slider.id}-value`);
        
        // Special handling for Age slider to update AgeGroup
        if (slider.id === 'Age') {
            const ageGroupSelect = document.getElementById('AgeGroup');
            
            slider.addEventListener('input', function() {
                const age = parseInt(this.value);
                
                // Update age display
                if (valueDisplay) {
                    valueDisplay.textContent = age;
                }
                
                // Update AgeGroup selector
                if (ageGroupSelect) {
                    const ageGroup = calculateAgeGroup(age);
                    ageGroupSelect.value = ageGroup;
                }
            });
        } else if (slider.id === 'MonthlyIncome') {
            // Special handling for MonthlyIncome slider to update SalarySlab
            const salarySlabSelect = document.getElementById('SalarySlab');
            
            slider.addEventListener('input', function() {
                const monthlyIncome = parseInt(this.value);
                
                // Update monthly income display
                if (valueDisplay) {
                    valueDisplay.textContent = monthlyIncome;
                }
                
                // Update SalarySlab selector
                if (salarySlabSelect) {
                    const salarySlab = calculateSalarySlab(monthlyIncome);
                    salarySlabSelect.value = salarySlab;
                }
            });
        } else {
            // Regular slider update
            slider.addEventListener('input', function() {
                if (valueDisplay) {
                    valueDisplay.textContent = this.value;
                }
            });
        }
        
        // Set initial value
        if (valueDisplay) {
            valueDisplay.textContent = slider.value;
        }
    });
    
    // Initialize AgeGroup based on initial Age value
    const ageSlider = document.getElementById('Age');
    const ageGroupSelect = document.getElementById('AgeGroup');
    if (ageSlider && ageGroupSelect) {
        const initialAge = parseInt(ageSlider.value);
        ageGroupSelect.value = calculateAgeGroup(initialAge);
    }
    
    // Initialize SalarySlab based on initial MonthlyIncome value
    const monthlyIncomeSlider = document.getElementById('MonthlyIncome');
    const salarySlabSelect = document.getElementById('SalarySlab');
    if (monthlyIncomeSlider && salarySlabSelect) {
        const initialMonthlyIncome = parseInt(monthlyIncomeSlider.value);
        salarySlabSelect.value = calculateSalarySlab(initialMonthlyIncome);
    }
}

// Initialize form submission
function initializeForm() {
    const form = document.getElementById('predictionForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        await predictAttrition();
    });
}

// Get form data
function getFormData() {
    const formData = {};
    const form = document.getElementById('predictionForm');
    const formElements = form.elements;
    
    for (let element of formElements) {
        if (element.name) {
            // Convert to appropriate type
            if (element.type === 'range' || element.type === 'number') {
                formData[element.name] = parseInt(element.value);
            } else {
                formData[element.name] = element.value;
            }
        }
    }
    
    return formData;
}

// Predict attrition
async function predictAttrition() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsContent = document.getElementById('resultsContent');
    const errorMessage = document.getElementById('errorMessage');
    
    // Show loading, hide results and errors
    loadingSpinner.style.display = 'block';
    resultsContent.style.display = 'none';
    errorMessage.style.display = 'none';
    
    try {
        // Get form data
        const formData = getFormData();
        
        // Make prediction request
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to make prediction. Please check your inputs and try again.');
    } finally {
        loadingSpinner.style.display = 'none';
    }
}

// Display prediction results
function displayResults(result) {
    const resultsContent = document.getElementById('resultsContent');
    const probabilityPercentage = document.getElementById('probabilityPercentage');
    const progressFill = document.getElementById('progressFill');
    const riskBadge = document.getElementById('riskBadge');
    const predictionText = document.getElementById('predictionText');
    
    // Update probability
    const probability = result.attrition_probability.toFixed(1);
    probabilityPercentage.textContent = `${probability}%`;
    progressFill.style.width = `${probability}%`;
    
    // Update risk level
    riskBadge.textContent = result.attrition_risk;
    riskBadge.className = 'risk-badge';
    
    if (result.attrition_risk === 'Low') {
        riskBadge.classList.add('risk-low');
    } else if (result.attrition_risk === 'Medium') {
        riskBadge.classList.add('risk-medium');
    } else if (result.attrition_risk === 'High') {
        riskBadge.classList.add('risk-high');
    }
    
    // Update prediction
    predictionText.textContent = result.prediction;
    predictionText.className = 'prediction-text';
    
    if (result.prediction === 'Will Stay') {
        predictionText.classList.add('prediction-stay');
    } else {
        predictionText.classList.add('prediction-leave');
    }
    
    // Show results with animation
    resultsContent.style.display = 'block';
    resultsContent.style.animation = 'fadeIn 0.5s';
    
    // Scroll to results on mobile
    if (window.innerWidth < 1200) {
        resultsContent.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// Show error message
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

// Add fade in animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

