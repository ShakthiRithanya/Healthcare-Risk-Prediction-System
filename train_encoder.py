import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import joblib

df = pd.read_csv("healthcare_dataset.csv")

categorical_columns = [
    "Gender", "Blood Type", "Medical Condition", 
    "Admission Type", "Medication", "Insurance Provider"
]

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
encoder.fit(df[categorical_columns])

joblib.dump(encoder, "encoder.pkl")
print("encoder.pkl created successfully!")
