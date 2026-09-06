import streamlit as st
import pandas as pd
import os
from agents.quality_agent import DataQualityAgent

st.set_page_config(
    page_title="Agentic Data Quality Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic Data Quality & Anomaly Detection System")
st.markdown("Automated hybrid data quality pipeline combining rule-based checks with AI-driven root cause analysis.")

# Initialize agent
data_path = "config/sample_transactions.csv"
if not os.path.exists(data_path):
    st.warning("Sample dataset not found. Please run data_generator.py first.")
else:
    agent = DataQualityAgent(data_path)
    report = agent.run_rule_based_checks()

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", report["total_rows"])
    col2.metric("Max Amount", f"${report['amount_max']:,.2f}")
    col3.metric("Invalid Status Count", len(report["invalid_statuses"]))

    st.subheader("📊 Raw Dataset Preview (With Anomalies)")
    st.dataframe(agent.df.head(15), use_container_width=True)

    st.subheader("🔍 Rule-Based Quality Report")
    st.json(report)

    if st.button("Run AI Quality Analysis (Groq LLM)"):
        with st.spinner("AI Agent is analyzing anomalies and root causes..."):
            ai_insights = agent.analyze_with_llm(report)
            st.success("Analysis Complete!")
            st.markdown("### 💡 AI Insights & Remediation Steps")
            st.write(ai_insights)