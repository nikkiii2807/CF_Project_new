import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import base64

# ----- App Config -----
st.set_page_config(page_title="Advanced Loan Predictor", page_icon="🏦", layout="centered")
st.title("🏦 Smart Loan Predictor & Financial Journey Game")

# ----- Tabs for different functionalities -----
tab1, tab2 = st.tabs(["Loan Predictor", "Financial Journey Game"])

with tab1:
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

        fig, ax = plt.subplots()
        ax.plot(scores, loans, color='purple')
        ax.set_xlabel('Credit Score')
        ax.set_ylabel('Loan Amount ($)')
        ax.set_title('Loan Amount vs Credit Score')
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


# ----- Financial Journey Game Tab -----
with tab2:
    st.header("💰 Financial Journey Game")
    st.markdown("""
    **Test your financial decision-making skills over 24 months!**
    
    Starting with ₹1,00,000, make monthly choices to grow your money:
    - 📈 **Invest**: Potential 10-20% returns, but risky
    - 🏦 **Save**: Safe 3-5% growth
    - 💸 **Borrow**: Get ₹10,000 now, but pay EMI later
    
    Watch out for market events that might affect your returns!
    """)
    
    # ----- Game Session State Setup -----
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
        
    if "game_data" not in st.session_state:
        st.session_state.game_data = {
            "month": 0,
            "money": [100000],  # ₹1L starting amount
            "events": [],
            "choices": [],
            "investment_amount": 0,
            "savings_amount": 0,
            "loan_amount": 0,
            "loan_emi": 0
        }
    
    # Market events with descriptions and impacts
    market_events = {
        "🔥 Inflation": {
            "description": "Rising prices reduce the value of your money!",
            "invest_impact": -0.02,  # -2% on investments
            "save_impact": -0.03,    # -3% on savings
            "probability": 0.25
        },
        "📉 Recession": {
            "description": "Economic downturn hits investments hard!",
            "invest_impact": -0.15,  # -15% on investments
            "save_impact": 0,        # No impact on savings
            "probability": 0.15
        },
        "🚀 Bull Run": {
            "description": "Markets are soaring! Great for investments!",
            "invest_impact": 0.25,   # +25% on investments
            "save_impact": 0,        # No impact on savings
            "probability": 0.15
        },
        "🧊 Stagnation": {
            "description": "Nothing much happening in the markets.",
            "invest_impact": 0.02,   # +2% on investments
            "save_impact": 0,        # No impact on savings
            "probability": 0.45
        }
    }
    
    # ----- Start Game Button -----
    if not st.session_state.game_started and st.button("🎮 Start New Game"):
        st.session_state.game_started = True
        st.session_state.game_data = {
            "month": 0,
            "money": [100000],
            "events": [],
            "choices": [],
            "investment_amount": 0,
            "savings_amount": 100000,  # Start with all money in savings
            "loan_amount": 0,
            "loan_emi": 0
        }
        st.rerun()  # Fixed: Changed from experimental_rerun() to rerun()
    
    if st.session_state.game_started:
        # Display current game status
        current_month = st.session_state.game_data["month"]
        current_money = st.session_state.game_data["money"][-1]
        
        # Game progress
        progress_percentage = current_month / 24
        st.progress(progress_percentage)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Month", f"{current_month}/24")
        with col2:
            st.metric("Current Net Worth", f"₹{current_money:,.2f}")
        with col3:
            if current_month > 0:
                previous_money = st.session_state.game_data["money"][-2]
                change = ((current_money - previous_money) / previous_money) * 100
                st.metric("Monthly Change", f"{change:+.2f}%")
            else:
                st.metric("Monthly Change", "0.00%")
        
        # Show portfolio breakdown
        st.subheader("📊 Your Portfolio")
        invest_amount = st.session_state.game_data["investment_amount"]
        save_amount = st.session_state.game_data["savings_amount"]
        loan_amount = st.session_state.game_data["loan_amount"]
        
        port_col1, port_col2, port_col3 = st.columns(3)
        with port_col1:
            st.metric("Investments", f"₹{invest_amount:,.2f}")
        with port_col2:
            st.metric("Savings", f"₹{save_amount:,.2f}")
        with port_col3:
            st.metric("Outstanding Loans", f"₹{loan_amount:,.2f}")
        
        # If game is still in progress (less than 24 months)
        if current_month < 24:
            # Show current month event if any
            if current_month > 0 and len(st.session_state.game_data["events"]) > 0:
                last_event = st.session_state.game_data["events"][-1]
                st.info(f"**Monthly Event:** {last_event} - {market_events[last_event]['description']}")
            
            # Monthly decision
            st.subheader(f"Month {current_month + 1}: Make Your Financial Decision")
            
            decision = st.radio(
                "What would you like to do this month?",
                ["Invest", "Save", "Borrow"],
                help="Invest for higher returns but with risk, Save for steady growth, or Borrow for immediate cash"
            )
            
            # Additional input based on decision
            if decision == "Invest":
                invest_percentage = st.slider("What percentage of your savings to invest?", 10, 100, 20)
                amount_to_invest = (invest_percentage / 100) * save_amount
                st.write(f"You'll invest ₹{amount_to_invest:,.2f} from your savings")
            elif decision == "Save":
                st.write("Your money will grow steadily in savings")
            elif decision == "Borrow":
                st.write("You'll receive ₹10,000 but will have to pay it back with interest")
            
            # Proceed to next month button
            if st.button("📅 Proceed to Next Month"):
                # Random market event
                event_names = list(market_events.keys())
                event_probabilities = [market_events[event]["probability"] for event in event_names]
                current_event = random.choices(event_names, weights=event_probabilities, k=1)[0]
                
                # Process financial decision
                if decision == "Invest":
                    amount_to_invest = (invest_percentage / 100) * save_amount
                    # Update portfolio
                    st.session_state.game_data["investment_amount"] += amount_to_invest
                    st.session_state.game_data["savings_amount"] -= amount_to_invest
                    
                    # Apply market event to investments
                    event_impact = market_events[current_event]["invest_impact"]
                    investment_return = st.session_state.game_data["investment_amount"] * (0.15 + event_impact)  # Base 15% + event impact
                    st.session_state.game_data["investment_amount"] += investment_return
                    
                elif decision == "Save":
                    # Apply market event to savings
                    event_impact = market_events[current_event]["save_impact"]
                    savings_return = st.session_state.game_data["savings_amount"] * (0.04 + event_impact)  # Base 4% + event impact
                    st.session_state.game_data["savings_amount"] += savings_return
                    
                elif decision == "Borrow":
                    # Add loan amount to savings
                    st.session_state.game_data["savings_amount"] += 10000
                    st.session_state.game_data["loan_amount"] += 10000
                    # Calculate EMI (simple calculation)
                    monthly_emi = 10000 * 1.12 / 12  # 12% annual interest, pay over 12 months
                    st.session_state.game_data["loan_emi"] += monthly_emi
                
                # Process EMI payment if any
                if st.session_state.game_data["loan_emi"] > 0:
                    st.session_state.game_data["savings_amount"] -= st.session_state.game_data["loan_emi"]
                    st.session_state.game_data["loan_amount"] -= (st.session_state.game_data["loan_emi"] * 0.8)  # 80% of EMI goes to principal
                
                # Calculate new total money
                new_total = st.session_state.game_data["investment_amount"] + st.session_state.game_data["savings_amount"] - st.session_state.game_data["loan_amount"]
                
                # Update game state
                st.session_state.game_data["month"] += 1
                st.session_state.game_data["money"].append(new_total)
                st.session_state.game_data["events"].append(current_event)
                st.session_state.game_data["choices"].append(decision)
                
                st.rerun()  # Fixed: Changed from experimental_rerun() to rerun()
        
        # Game over - show results
        else:
            st.balloons()
            st.success("🎉 Game Completed! Here's your 24-month financial journey summary:")
            
            # Calculate final metrics
            initial_money = st.session_state.game_data["money"][0]
            final_money = st.session_state.game_data["money"][-1]
            total_growth = ((final_money - initial_money) / initial_money) * 100
            
            # Count decisions made
            decision_counts = {
                "Invest": st.session_state.game_data["choices"].count("Invest"),
                "Save": st.session_state.game_data["choices"].count("Save"),
                "Borrow": st.session_state.game_data["choices"].count("Borrow")
            }
            
            # Determine financial personality
            if decision_counts["Invest"] > 15:
                personality = "Bold Investor 🚀"
                personality_desc = "You're not afraid of risk and aim for big returns!"
            elif decision_counts["Save"] > 15:
                personality = "Safe Saver 🛡️"
                personality_desc = "You prioritize stability and steady growth."
            elif decision_counts["Borrow"] > 10:
                personality = "Leverage Lover 💳"
                personality_desc = "You use loans strategically to boost your growth."
            else:
                personality = "Balanced Planner ⚖️"
                personality_desc = "You take a diversified approach to finances."
            
            # Calculate risk score (0-100)
            risk_score = (decision_counts["Invest"] * 4 + decision_counts["Borrow"] * 5) / 24
            risk_score = min(risk_score * 10, 100)  # Scale to 0-100
            
            # Display results
            st.header("📊 Your Financial Journey Results")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Starting Amount", f"₹{initial_money:,.2f}")
                st.metric("Final Net Worth", f"₹{final_money:,.2f}", f"{total_growth:+.2f}%")
                
                # Risk meter
                st.subheader("Risk Score")
                st.progress(risk_score/100)
                st.write(f"**{risk_score:.1f}/100**")
                
            with col2:
                st.subheader("Financial Personality")
                st.info(f"**{personality}**")
                st.write(personality_desc)
                
                # Decision breakdown
                st.subheader("Your Decisions")
                fig, ax = plt.subplots()
                ax.pie(
                    [decision_counts["Invest"], decision_counts["Save"], decision_counts["Borrow"]], 
                    labels=["Invest", "Save", "Borrow"],
                    autopct='%1.1f%%',
                    colors=['#ff9999','#66b3ff','#99ff99']
                )
                ax.set_title('Your Financial Choices')
                st.pyplot(fig)
            
            # Growth chart
            st.subheader("📈 Your Net Worth Over Time")
            fig, ax = plt.subplots(figsize=(10, 6))
            months = range(1, 25)
            ax.plot(months, st.session_state.game_data["money"], marker='o', linewidth=2)
            
            # Mark events on the chart
            for i, event in enumerate(st.session_state.game_data["events"]):
                if "Bull Run" in event:
                    ax.axvspan(i+1, i+2, alpha=0.2, color='green')
                elif "Recession" in event:
                    ax.axvspan(i+1, i+2, alpha=0.2, color='red')
            
            ax.set_xlabel('Month')
            ax.set_ylabel('Net Worth (₹)')
            ax.set_title('24-Month Financial Journey')
            ax.grid(True)
            st.pyplot(fig)
            
            # Financial journey table
            st.subheader("Month-by-Month Journey")
            
            # Create a dataframe for the journey
            journey_data = {
                "Month": list(range(1, 25)),
                "Net Worth": st.session_state.game_data["money"],
                "Decision": ["Starting Point"] + st.session_state.game_data["choices"],
                "Market Event": ["None"] + st.session_state.game_data["events"]
            }
            
            # Show the journey table
            st.write("Here's your financial journey throughout the game:")
            for i in range(len(journey_data["Month"])):
                with st.expander(f"Month {journey_data['Month'][i]} - ₹{journey_data['Net Worth'][i]:,.2f}"):
                    st.write(f"**Decision:** {journey_data['Decision'][i]}")
                    if i > 0:  # Skip first month as it has no event
                        event = journey_data['Market Event'][i]
                        st.write(f"**Event:** {event} - {market_events.get(event, {'description': 'None'})['description']}")
            
            # Play again button
            if st.button("🔄 Play Again"):
                st.session_state.game_data = {
                    "month": 0,
                    "money": [100000],
                    "events": [],
                    "choices": [],
                    "investment_amount": 0,
                    "savings_amount": 100000,
                    "loan_amount": 0,
                    "loan_emi": 0
                }
                st.rerun()  # Fixed: Changed from experimental_rerun() to rerun()
    
    # If game not started, show instructions
    else:
        st.info("""
        ## How to Play:
        1. Start with ₹1,00,000
        2. Each month, choose one financial action: Invest, Save, or Borrow
        3. Random market events will affect your returns
        4. After 24 months, see your final net worth and financial personality
        
        Click "Start New Game" to begin your financial journey!
        """)
        
        # Show example market events
        st.subheader("Possible Market Events")
        for event, details in market_events.items():
            st.write(f"**{event}:** {details['description']}")
            
        # Show expected returns
        st.subheader("Expected Returns")
        st.markdown("""
        - **Invest**: 10-20% potential return, but can go negative during recession
        - **Save**: 3-5% steady growth, lower impact from market events
        - **Borrow**: Get ₹10,000 immediately, but pay 12% annual interest
        """)