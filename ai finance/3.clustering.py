import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Load data
X_scaled = np.load("data/processed_data.npy")

# Elbow method
inertia = []

K = range(1, 10)

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

# Plot
plt.plot(K, inertia, marker='o')
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.show()