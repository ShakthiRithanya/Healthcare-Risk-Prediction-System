import pandas as pd
import joblib

# Load your dataset
df = pd.read_csv("healthcare_dataset.csv")

# Select only meaningful columns for ML
selected_columns = [
    "Age", "Gender", "Blood Type", "Medical Condition",
    "Billing Amount", "Admission Type", "Medication", "Insurance Provider"
]

df = df[selected_columns]

# One-hot encode categorical columns
df_encoded = pd.get_dummies(df)

# Save the final columns list for Flask app
feature_columns = df_encoded.columns.tolist()
joblib.dump(feature_columns, "feature_columns.pkl")

print("feature_columns.pkl created with", len(feature_columns), "columns")
