import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import plotly.graph_objects as go


# Title Section
st.title("💰 Financial Resilience Navigator")
st.markdown("""
This interactive app helps you assess your financial resilience.  
Enter your details below and visualize how long it will take to build your emergency fund!
""")
st.divider()

# Sidebar for user inputs
st.sidebar.header("📊 Input Your Financial Data")
monthly_income = st.sidebar.number_input("Monthly Income ($)", min_value=0.0, value=5000.0, step=100.0)
monthly_expenses = st.sidebar.number_input("Monthly Expenses ($)", min_value=0.0, value=3000.0, step=50.0)
current_savings = st.sidebar.number_input("Current Savings ($)", min_value=0.0, value=10000.0, step=100.0)
current_debt = st.sidebar.number_input("Current Debt ($)", min_value=0.0, value=5000.0, step=100.0)
desired_coverage_months = st.sidebar.slider("Desired Emergency Fund Coverage (Months)", min_value=1, max_value=12, value=6)

# Additional options
st.sidebar.markdown("---")
annual_return_rate = st.sidebar.slider("Expected Annual Return Rate (%)", min_value=0.0, max_value=20.0, value=4.0) / 100

# Financial Calculations
monthly_surplus = monthly_income - monthly_expenses
target_emergency_fund = monthly_expenses * desired_coverage_months
monthly_rate = (1 + annual_return_rate) ** (1/12) - 1

# Simulation: Calculate Savings Growth
months_needed = 0
savings = current_savings
savings_history = [savings]

if monthly_surplus <= 0:
    st.error("❗ Your monthly surplus is non-positive. Consider adjusting your budget!")
else:
    while savings < target_emergency_fund:
        months_needed += 1
        savings = (savings + monthly_surplus) * (1 + monthly_rate)
        savings_history.append(savings)

    st.subheader("📅 Emergency Fund Goal Timeline")
    st.success(f"✅ Estimated Time to Reach Target: **{months_needed} months**")

    # Motivational Tip
    if months_needed <= 6:
        st.success("🚀 Great job! You're on track to achieve your goal quickly.")
    elif months_needed <= 12:
        st.info("💡 Consider minor adjustments for faster savings.")
    else:
        st.warning("⏳ It may take longer than ideal — consider reviewing expenses or increasing your income.")

# Improved Savings Trajectory Graph
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=list(range(months_needed + 1)), 
    y=savings_history, 
    mode='lines+markers', 
    name='Savings Growth',
    line=dict(color='#4CAF50', width=3),
    marker=dict(size=8)
))

# Target Fund Line
fig.add_trace(go.Scatter(
    x=[0, months_needed],
    y=[target_emergency_fund] * 2,
    mode='lines',
    name='Target Emergency Fund',
    line=dict(color='#FF5733', dash='dash')
))

# Progress Milestones
if months_needed > 0:
    fig.add_trace(go.Scatter(
        x=[months_needed // 2], 
        y=[savings_history[months_needed // 2]], 
        mode='markers+text',
        marker=dict(size=12, color='gold'),
        text=['50% Milestone'],
        textposition='top center'
    ))

fig.update_layout(
    title="🚀 Savings Trajectory Over Time",
    xaxis_title="Months",
    yaxis_title="Total Savings ($)",
    template="plotly_dark",
    margin=dict(l=40, r=40, t=40, b=40)
)

st.plotly_chart(fig)

# Downloadable PDF Report
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, "Financial Resilience Navigator Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, f"Estimated Time to Reach Target: {months_needed} months", ln=True)
    pdf.cell(200, 10, f"Monthly Income: ${monthly_income:,.2f}", ln=True)
    pdf.cell(200, 10, f"Monthly Expenses: ${monthly_expenses:,.2f}", ln=True)
    pdf.cell(200, 10, f"Current Savings: ${current_savings:,.2f}", ln=True)
    pdf.cell(200, 10, f"Current Debt: ${current_debt:,.2f}", ln=True)

    pdf_path = "financial_report.pdf"
    pdf.output(pdf_path)
    return pdf_path

if st.button("📝 Download Financial Report"):
    pdf_path = generate_pdf()
    with open(pdf_path, "rb") as file:
        st.download_button(label="Download PDF", data=file, file_name="Financial_Resilience_Report.pdf", mime="application/pdf")

st.markdown("---")

# Final Tips and Insights
st.markdown("### 💡 How Does This App Help?")
st.info("""
- **Risk Profiling:** Understand if your current savings strategy is enough for emergencies.  
- **Scenario Analysis:** Adjust parameters to test different financial outcomes.  
- **Visual Insights:** The savings graph illustrates progress toward your financial goals.
""")
