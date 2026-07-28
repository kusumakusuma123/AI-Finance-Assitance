import pandas as pd

df = pd.read_csv(r"C:\Users\kusuma\OneDrive\Desktop\AI FINANCE ASSISTANT\ai finance")

# Select important columns
df = df[['age', 'monthly_income', 'savings_rate', 'debt',
         'housing_expense', 'food_expense', 'transport_expense',
         'entertainment_expense', 'shopping_expense',
         'healthcare_expense', 'credit_card_usage',
         'financial_stress', 'financial_health_score']]

print(df.head())

print(df.isnull().sum())

# Fill missing values (simple method)
df = df.fillna(df.mean(numeric_only=True))

df['financial_stress'] = df['financial_stress'].map({
    'Low': 0,
    'Medium': 1,
    'High': 2
})

print(df['credit_card_usage'].unique())
df['credit_card_usage'] = df['credit_card_usage'].map({
    'Low': 0,
    'Medium': 1,
    'High': 2
})

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_scaled = scaler.fit_transform(df)

print(X_scaled.shape)

import numpy as np
import os

# Ensure folders exist
os.makedirs("data", exist_ok=True)


# Save processed data
np.save("data/processed_data.npy", X_scaled)

print("✅ Processed data saved successfully!")