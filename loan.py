import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import base64

# ----- App Config -----
st.set_page_config(page_title="Advanced Loan Predictor", page_icon="🏦", layout="centered")
st.title("🏦 Smart Loan Amount Predictor (Enhanced + Loan Genie)")

st.markdown("""
Welcome to the Loan Predictor App.  
Fill in your details to check your estimated loan eligibility, get personalized tips, and find government loan schemes!  
""")

# ----- Session State Setup -----
if "predicted" not in st.session_state:
    st.session_state.predicted = False

# ----- Sidebar Inputs -----
st.sidebar.header("🔧 Enter Your Details:")

income = st.sidebar.slider("Monthly Income ($)", 1000, 20000, 5000)
age = st.sidebar.slider("Age", 18, 70, 30)
loan_term = st.sidebar.selectbox("Loan Term (Years)", [5, 10, 15, 20, 25, 30])
credit_score = st.sidebar.slider("Credit Score", 300, 850, 650)
employment_status = st.sidebar.selectbox("Employment Status", ["Employed", "Self-Employed", "Unemployed"])
loan_type = st.sidebar.selectbox("Loan Type", ["Home Loan", "Car Loan", "Education Loan", "Personal Loan"])
occupation = st.sidebar.selectbox("Occupation", ["Salaried", "Entrepreneur", "Farmer", "Student", "Retired"])

employment_map = {"Employed": 1, "Self-Employed": 0.8, "Unemployed": 0.5}
employment_factor = employment_map[employment_status]

loan_type_map = {
    "Home Loan": 1.2,
    "Car Loan": 0.8,
    "Education Loan": 0.9,
    "Personal Loan": 0.7
}
loan_type_factor = loan_type_map[loan_type]

# ----- Predict Button -----
if st.sidebar.button("🔮 Predict Loan Amount"):
    st.session_state.predicted = True

# ----- Prediction & Output -----
if st.session_state.predicted:
    st.subheader("📊 Prediction Results")

    loan_amount = (income * 10) * (credit_score / 850) * employment_factor * loan_type_factor / (loan_term / 10)
    approval_chance = (credit_score / 850) * 100

    st.success(f"Estimated Loan Amount: ${loan_amount:,.2f}")
    st.info(f"Approval Chance: {approval_chance:.1f}%")

    # Loan vs Credit Score Plot
    st.subheader("📈 Loan Eligibility vs Credit Score")
    scores = np.linspace(300, 850, 100)
    loans = (income * 10) * (scores / 850) * employment_factor * loan_type_factor / (loan_term / 10)

    # fig, ax = plt.subplots()
    # ax.plot(scores, loans, color='purple')
    # ax.set_xlabel('Credit Score')
    # ax.set_ylabel('Loan Amount ($)')
    # ax.set_title('Loan Amount vs Credit Score')
    # st.pyplot(fig)

    import plotly.graph_objects as go

    #st.subheader("📊 Interactive: Loan Amount vs Credit Score")

    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(x=scores, y=loans, mode='lines', line=dict(color='purple')))
    fig7.update_layout(
        xaxis_title='Credit Score',
        yaxis_title='Loan Amount ($)',
        #title='Loan Amount vs Credit Score (Interactive)',
        template='plotly_dark'
    )
    st.plotly_chart(fig7)



    import seaborn as sns

    st.subheader("🔥 Heatmap: Credit Score vs Predicted Loan Amount")

    # Create ranges
    cs_range = np.arange(300, 851, 50)
    income_range = np.arange(1000, 20001, 1000)

    # Generate a 2D matrix
    heat_data = []
    for income_val in income_range:
        row = []
        for cs_val in cs_range:
            amt = (income_val * 10) * (cs_val / 850) * employment_factor * loan_type_factor / (loan_term / 10)
            row.append(amt)
        heat_data.append(row)

    # Convert to DataFrame for seaborn
    import pandas as pd
    df_heat = pd.DataFrame(heat_data, index=income_range, columns=cs_range)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df_heat, cmap="YlGnBu", ax=ax, cbar_kws={'label': 'Loan Amount ($)'}, linewidths=0.5)

    ax.set_title("Credit Score vs Income vs Predicted Loan Amount")
    ax.set_xlabel("Credit Score")
    ax.set_ylabel("Monthly Income ($)")
    st.pyplot(fig)

    # Metrics
    st.subheader("💡 Insights:")
    st.metric(label="Monthly EMI (Estimate)", value=f"${loan_amount / (loan_term*12):.2f}")
    st.metric(label="Loan Term (Years)", value=f"{loan_term} Years")
    st.metric(label="Predicted Approval", value=f"{approval_chance:.1f}%")

    # Scheme Recommender
    st.subheader("🧞‍♂️ Loan Genie: Govt Subsidized Schemes for You")
    schemes = {
        "Student": [
            "Vidya Lakshmi Education Loan (Interest Subsidy)",
            "National Overseas Scholarship for Higher Education",
            "Central Sector Interest Subsidy Scheme (CSIS)"
        ],
        "Entrepreneur": [
            "MUDRA Loans under PMMY",
            "Stand Up India Scheme",
            "Startup India Seed Fund Scheme"
        ],
        "Farmer": [
            "Kisan Credit Card (KCC) Scheme",
            "PM-KISAN Credit Subsidy",
            "Agriculture Infrastructure Fund Loan"
        ],
        "Salaried": [
            "PMAY Subsidized Home Loan",
            "Affordable Housing Interest Subsidy Scheme",
            "Subsidized Auto Loan for E-Vehicles"
        ],
        "Retired": [
            "Senior Citizen Savings Scheme (SCSS)",
            "Reverse Mortgage Loan Subsidy",
            "Pension Loan Facility by Nationalized Banks"
        ]
    }

    recommended = random.sample(schemes.get(occupation, []), 3)
    for i, scheme in enumerate(recommended, 1):
        st.info(f"{i}. {scheme}")

    st.subheader("📋 Suggested Documents to Prepare:")
    st.markdown("""
    - Identity Proof (Aadhar / Passport / Driving License)  
    - Address Proof (Utility Bills / Rent Agreement)  
    - Income Proof (Salary Slips / IT Returns)  
    - Bank Statements (Last 6 months)  
    - Educational Proof (if Education Loan)  
    - Land Ownership Proof (if Agriculture Loan)  
    """)

    st.subheader("⚡ Risk Meter")
    if credit_score > 750:
        st.success("Low Risk: Great Credit Score!")
    elif 600 < credit_score <= 750:
        st.warning("Moderate Risk: Improve your Credit Score for better rates.")
    else:
        st.error("High Risk: Loan approval may be difficult. Consider credit repair steps.")

    # Download Report
    st.subheader("📄 Download Your Loan Report")
    report = f"""
    Loan Prediction Report:
    - Income: ${income}
    - Age: {age}
    - Employment Status: {employment_status}
    - Loan Type: {loan_type}
    - Predicted Loan Amount: ${loan_amount:,.2f}
    - Approval Chance: {approval_chance:.1f}%
    - Recommended Schemes: {', '.join(recommended)}
    """
    b64 = base64.b64encode(report.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="loan_report.txt">📥 Download Report</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Decision Simulator
    st.subheader("🧠 Should I Take This Loan? – Decision Simulator")
    st.markdown("Adjust the values below to simulate how taking a loan might affect your financial future.")

    sim_loan_amount = st.slider("Loan Amount ($)", 1000, 200000, int(loan_amount), key="sim_loan_amt")
    sim_income = st.slider("Monthly Income ($)", 1000, 20000, income, key="sim_income")
    sim_duration = st.slider("Loan Term (Years)", 1, 30, loan_term, key="sim_term")
    sim_interest = st.slider("Interest Rate (%)", 5.0, 15.0, 8.0, key="sim_interest")

    monthly_interest_rate = sim_interest / (12 * 100)
    n_payments = sim_duration * 12

    try:
        emi = (sim_loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**n_payments) / \
              ((1 + monthly_interest_rate)**n_payments - 1)
    except ZeroDivisionError:
        emi = 0

    debt_ratio = (emi / sim_income) * 100
    net_savings = (sim_income - emi) * n_payments

    st.metric("📉 Estimated EMI", f"${emi:,.2f}")
    st.metric("📊 Debt-to-Income Ratio", f"{debt_ratio:.2f}%")
    st.metric("💰 Net Savings After Loan Term", f"${net_savings:,.2f}")

    # Recommendation
    st.subheader("🧾 Loan Impact Analysis")
    if debt_ratio < 30:
        st.success("✅ You can comfortably afford this loan.")
    elif 30 <= debt_ratio < 50:
        st.warning("⚠️ Think carefully. This loan might stretch your finances.")
    else:
        st.error("❌ High debt risk! Consider reducing the loan amount or increasing the term.")

    # Graph
    st.subheader("📉 Net Worth & EMI Over Time")
    months = np.arange(1, n_payments + 1)
    cumulative_savings = np.cumsum([sim_income - emi] * n_payments)
    emi_line = [emi] * n_payments

    fig2, ax2 = plt.subplots()
    ax2.plot(months, cumulative_savings, label="Net Savings Over Time", color='green')
    ax2.plot(months, emi_line, label="Monthly EMI", linestyle='--', color='red')
    ax2.set_xlabel("Months")
    ax2.set_ylabel("Amount ($)")
    ax2.set_title("Financial Simulation Over Loan Period")
    ax2.legend()
    st.pyplot(fig2)

    st.subheader("📊 Debt Burden To Income Ratio")

    # Define dynamic range: only up to sim_duration (+ optional few more years if you want)
    max_term = sim_duration + 5 if sim_duration + 5 <= 30 else 30
    terms_dynamic = np.arange(1, max_term + 1)

    dynamic_emis = []
    dynamic_ratios = []
    dynamic_savings = []

    for term in terms_dynamic:
        n = term * 12
        r = sim_interest / (12 * 100)
        
        try:
            emi_val = (sim_loan_amount * r * (1 + r)**n) / ((1 + r)**n - 1)
        except ZeroDivisionError:
            emi_val = 0
        
        debt_ratio_val = (emi_val / sim_income) * 100
        net_saving_val = (sim_income - emi_val) * n

        dynamic_emis.append(emi_val)
        dynamic_ratios.append(debt_ratio_val)
        dynamic_savings.append(net_saving_val)

    # Plotting the dynamic range
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.plot(terms_dynamic, dynamic_ratios, marker='o', color='orange', label="Debt-to-Income Ratio (%)")
    ax4.axvline(sim_duration, color='red', linestyle='--', label=f"Selected Term ({sim_duration} yrs)")
    ax4.set_xlabel("Loan Term (Years)")
    ax4.set_ylabel("Debt-to-Income Ratio (%)")
    ax4.set_title("📉 Financial Impact of Loan Duration")
    ax4.grid(True)
    ax4.legend()
    st.pyplot(fig4)

    # Optional table for breakdown
    import pandas as pd
    loan_analysis_df = pd.DataFrame({
        "Loan Term (Years)": terms_dynamic,
        "EMI ($)": [f"{e:,.2f}" for e in dynamic_emis],
        "Debt-to-Income (%)": [f"{d:.2f}" for d in dynamic_ratios],
        "Net Savings ($)": [f"{s:,.2f}" for s in dynamic_savings],
    })

    st.subheader("📄 Term-wise Financial Breakdown")
    st.dataframe(loan_analysis_df, use_container_width=True)


# Loan Literacy Game
st.subheader("🎮 Gamified Loan Literacy Challenge")
st.markdown("Complete Levels to Escape the Debt Spiral!")

with st.expander("📘 Level 1: What's a Good Credit Score?"):
    st.write("Your score is 720. Is this good?")
    if st.button("🟢 Yes, it's good (Level 1)"):
        st.success("Correct! 720+ is generally considered a good score.")

with st.expander("💰 Level 2: EMI Trap"):
    st.write("You get an offer for a 0% EMI phone. What should you check?")
    if st.button("🔍 Check hidden charges (Level 2)"):
        st.success("Correct! There may be hidden processing fees or inflated MRP.")

with st.expander("📈 Level 3: Interest Game"):
    st.write("Is 6% interest on reducing balance better than 5% flat interest?")
    if st.button("✔️ Yes, reducing is better (Level 3)"):
        st.success("Correct! Reducing interest means you pay less over time.")

st.markdown("🚀 Complete all levels to become a Loan Master!")

# Optional Reset
if st.button("🔄 Reset Prediction"):
    st.session_state.predicted = False
