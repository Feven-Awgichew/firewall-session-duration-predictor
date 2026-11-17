"""
Run the code below in your REGRESSION NOTEBOOK after the selected
Random Forest pipeline has been fitted.

IMPORTANT:
- `rf_reduced_model` must be the fitted pipeline that includes both
  preprocessing (including the fitted encoder) and the Random Forest.
- It must expect the columns:
    1. Action
    2. NAT Destination Port

If your fitted pipeline has a different variable name, replace
`rf_reduced_model` with that exact variable name.
"""

from pathlib import Path
import joblib

# Create the models directory inside the Streamlit project folder.
Path("models").mkdir(exist_ok=True)

# Save the complete fitted pipeline, not only the Random Forest estimator.
joblib.dump(
    rf_reduced_model,
    "models/firewall_duration_model.joblib"
)

print("Model exported to models/firewall_duration_model.joblib")
