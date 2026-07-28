import streamlit as st
import numpy as np
import joblib
import pandas as pd

# ------------------ LOGIN SYSTEM ------------------
def login():
    st.markdown("<h2 style='text-align:center;'>🔐AI Finance Assistant</h2>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
        else:
            st.error("Invalid Credentials")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ------------------ STYLING ------------------
st.markdown("""
<style>
.main { background-color: black; }
div.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    background: linear-gradient(to right, #4CAF50, #2E8B57);
    color: white;
}
div.stButton > button:hover {
    background: linear-gradient(to right, #45a049, #1e6f43);
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("<h1 style='text-align:center;'>💰 Investment Recommendation System</h1>", unsafe_allow_html=True)

# ------------------ INPUT ------------------
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 70)
    income = st.number_input("Monthly Income", min_value=0)
    savings_rate = st.slider("Savings Rate", 0.0, 1.0)
    debt = st.number_input("Debt")
    credit_card = st.selectbox("Credit Card Usage", ["Low", "Medium", "High"])

with col2:
    housing = st.number_input("Housing Expense")
    food = st.number_input("Food Expense")
    transport = st.number_input("Transport Expense")
    entertainment = st.number_input("Entertainment Expense")
    shopping = st.number_input("Shopping Expense")
    healthcare = st.number_input("Healthcare Expense")
    stress = st.selectbox("Financial Stress", ["Low", "Medium", "High"])
    health_score = st.number_input("Financial Health Score")

# ------------------ MAP ------------------
cc_map = {"Low": 0, "Medium": 1, "High": 2}
stress_map = {"Low": 0, "Medium": 1, "High": 2}

credit_card = cc_map[credit_card]
stress = stress_map[stress]

# ------------------ LOAD MODEL ------------------
kmeans = joblib.load("models/kmeans.pkl")
scaler = joblib.load("models/scaler.pkl")

# ------------------ VALIDATION ------------------
def validate_inputs(income, savings_rate, debt, health_score):
    if income <= 0:
        return "Income must be greater than 0"
    if savings_rate < 0 or savings_rate > 1:
        return "Savings rate must be between 0 and 1"
    if debt < 0:
        return "Debt cannot be negative"
    if health_score <= 0:
        return "Enter valid financial health score"
    return None

# ------------------ RULE ENGINE ------------------
def rule_based_risk(age, income, savings_rate, debt, expenses, stress, health_score):

    total_expense = sum(expenses)
    expense_ratio = total_expense / income if income > 0 else 1

    if debt > income * 2 or expense_ratio > 0.9:
        return "Conservative"

    if savings_rate < 0.2 and stress == 2:
        return "Conservative"

    if savings_rate > 0.4 and health_score > 25 and debt < income * 0.5:
        return "Aggressive"

    if 0.2 <= savings_rate <= 0.4 and health_score >= 15:
        return "Moderate"

    return "Moderate"

# ------------------ FINAL DECISION ------------------
def final_risk_decision(rule_risk, model_risk, savings_rate, debt, income):

    if debt > income:
        return "Conservative"

    if rule_risk == model_risk:
        return rule_risk

    if savings_rate > 0.4:
        return "Aggressive"

    if savings_rate < 0.2:
        return "Conservative"

    return "Moderate"

# ------------------ PORTFOLIO ------------------
def dynamic_portfolio(risk, savings_rate, health_score):

    if risk == "Conservative":
        stocks, bonds, mf, gold = 20, 40, 25, 15
    elif risk == "Moderate":
        stocks, bonds, mf, gold = 40, 20, 25, 15
    else:
        stocks, bonds, mf, gold = 60, 10, 20, 17

    if savings_rate > 0.4:
        stocks += 10
        bonds -= 5
    elif savings_rate < 0.2:
        stocks -= 10
        bonds += 10

    if health_score > 25:
        stocks += 5
        mf += 5
    elif health_score < 15:
        bonds += 15
        gold += 5

    total = stocks + bonds + mf + gold

    return {
        "Stocks": round((stocks/total)*100),
        "Mutual Funds": round((mf/total)*100),
        "Bonds": round((bonds/total)*100),
        "Gold": round((gold/total)*100)
    }

# ------------------ NEW: EXPECTED RETURN ------------------
def expected_return(risk):
    if risk == "Conservative":
        return "5–7%"
    elif risk == "Moderate":
        return "8–10%"
    else:
        return "12–15%"

# ------------------ NEW: SIP CALCULATION ------------------
def calculate_sip(income, savings_rate):
    sip = income * savings_rate * 0.4
    return int(round(sip, -2))

# ------------------ BUTTON ------------------
col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])
with col_btn2:
    predict_btn = st.button(" Get Recommendation")

# ------------------ ACTION ------------------
if predict_btn:

    error = validate_inputs(income, savings_rate, debt, health_score)
    if error:
        st.error(error)
        st.stop()

    columns = [
        'age','monthly_income','savings_rate','debt',
        'housing_expense','food_expense','transport_expense',
        'entertainment_expense','shopping_expense',
        'healthcare_expense','credit_card_usage',
        'financial_stress','financial_health_score'
    ]

    input_df = pd.DataFrame([[ 
        age, income, savings_rate, debt,
        housing, food, transport,
        entertainment, shopping, healthcare,
        credit_card, stress, health_score
    ]], columns=columns)

    # ML prediction
    scaled = scaler.transform(input_df)
    cluster = kmeans.predict(scaled)[0]

    cluster_map = {
        0: "Moderate",
        1: "Aggressive",
        2: "Conservative"
    }

    model_risk = cluster_map[cluster]

    # Rule prediction
    expenses = [housing, food, transport, entertainment, shopping, healthcare]

    rule_risk = rule_based_risk(
        age, income, savings_rate, debt,
        expenses, stress, health_score
    )

    # Final decision
    final_risk = final_risk_decision(
        rule_risk, model_risk,
        savings_rate, debt, income
    )

    # Portfolio
    portfolio = dynamic_portfolio(final_risk, savings_rate, health_score)

    # NEW dynamic outputs
    ret = expected_return(final_risk)
    sip = calculate_sip(income, savings_rate)

    # ------------------ OUTPUT ------------------
    st.subheader("📊 Results")

    c1, c2, c3 = st.columns(3)
    c1.metric("Rule-Based", rule_risk)
    c2.metric("ML Model", model_risk)
    c3.metric("Final Decision", final_risk)

    st.write("### Portfolio Allocation")
    st.write(portfolio)
    st.bar_chart(portfolio)

    st.info(f"📈 Expected Return: {ret}")
    st.info(f"💡 Suggested SIP: ₹{sip}/month")