import numpy as np
from sklearn.cluster import KMeans
import joblib
import os

# Load data
X_scaled = np.load("data/processed_data.npy")

# Train model with K=3
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_scaled)

"""# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(kmeans, "models/kmeans.pkl")

print("✅ Model trained and saved!")"""
# Get cluster labels
labels = kmeans.labels_

# Print first 10 labels
print("First 10 cluster labels:")
print(labels[:10])

import pandas as pd

# Load original dataset
df = pd.read_csv(r"C:\Users\rgukt\OneDrive\Desktop\deeraj_project\personal_spending_dataset.csv")

# Add cluster labels
df['cluster'] = labels

# See average values of each cluster
cluster_summary = df.groupby('cluster').mean(numeric_only=True)

print("\nCluster Summary:")
print(cluster_summary)

# Map clusters to risk profiles
cluster_map = {
    0: "Moderate",
    1: "Aggressive",
    2: "Conservative"
}

df['risk_profile'] = df['cluster'].map(cluster_map)

print("\nSample with Risk Profile:")
print(df[['cluster', 'risk_profile']].head())

df.to_csv("data/final_clustered_data.csv", index=False)
print("✅ Final dataset saved!")