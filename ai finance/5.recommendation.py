import numpy as np
import joblib

# Load model and scaler
kmeans = joblib.load("models/kmeans.pkl")
scaler = joblib.load("models/scaler.pkl")

# Example user input
age = 25
income = 50000
savings_rate = 0.3
debt = 10000

housing = 10000
food = 5000
transport = 3000
entertainment = 2000
shopping = 3000
healthcare = 2000

credit_card = 1   # (Low=0, Medium=1, High=2)
stress = 1        # (Low=0, Medium=1, High=2)
health_score = 20

input_data = np.array([[age, income, savings_rate, debt,
                        housing, food, transport,
                        entertainment, shopping, healthcare,
                        credit_card, stress, health_score]])

scaled_input = scaler.transform(input_data)

cluster = kmeans.predict(scaled_input)[0]

print("Predicted Cluster:", cluster)

cluster_map = {
    0: "Moderate",
    1: "Aggressive",
    2: "Conservative"
}

risk = cluster_map[cluster]

print("Risk Profile:", risk)

def recommend_portfolio(risk):
    
    if risk == "Conservative":
        return {"Bonds": 60, "Mutual Funds": 25, "Gold": 10, "Stocks": 5}
    
    elif risk == "Moderate":
        return {"Mutual Funds": 40, "Stocks": 30, "Bonds": 20, "Gold": 10}
    
    else:
        return {"Stocks": 60, "Mutual Funds": 25, "Gold": 10, "Bonds": 5}

portfolio = recommend_portfolio(risk)

print("\n📊 Final Recommendation:")
print("Risk:", risk)
print("Portfolio:", portfolio)