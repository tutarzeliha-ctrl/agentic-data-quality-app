import streamlit as st
import pandas as pd
import os
from agents.quality_agent import DataQualityAgent
from connectors.base_connector import DataConnector
from metadata.tracker import MetadataTracker

st.set_page_config(
    page_title="Agentic Data Quality Platform",
    page_icon="🤖",
    layout="wide"
)

# Initialize Metadata Tracker
tracker = MetadataTracker()

st.title("🤖 Enterprise Agentic Data Quality & Anomaly Detection")
st.markdown("Automated hybrid data quality pipeline combining rule-based checks with AI-driven root cause analysis and metadata tracking.")

# Sidebar Controls
st.sidebar.header("Pipeline Configuration")
source_option = st.sidebar.selectbox("Select Data Source", ["Local CSV", "Custom Upload"])

data_path = "sample_data.csv"
if source_option == "Custom Upload":
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        data_path = "uploaded_temp.csv"
        with open(data_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

# Run Quality Check Button
if st.sidebar.button("Run Quality Pipeline & AI Analysis", type="primary"):
    with st.spinner("Executing pipeline, validating rules, and invoking AI agent..."):
        try:
            # 1. Load Data via Connector
            connector = DataConnector("csv", data_path)
            df = connector.load_data()
            
            # 2. Run Quality Agent
            agent = DataQualityAgent(data_path)
            report = agent.run_validation()
            
            # 3. Calculate metrics for logging
            total_rows = len(df)
            missing_vals = int(df.isnull().sum().sum())
            invalid_status = int((df['status'] == 'UNKNOWN').sum()) if 'status' in df.columns else 0
            
            # Quality score heuristic
            quality_score = max(0.0, 100.0 - ((missing_vals + invalid_status) / (total_rows * max(1, len(df.columns))) * 100))
            
            # 4. Log to Metadata Store
            tracker.log_run(total_rows, missing_vals, invalid_status, quality_score)
            
            st.success("Pipeline executed successfully and metrics logged to metadata store!")
            
            # Display Results
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Rows", total_rows)
            col2.metric("Missing Values", missing_vals)
            col3.metric("Calculated Quality Score", f"{quality_score:.2f}%")
            
            st.subheader("📊 Dataset Preview")
            st.dataframe(df.head(10))
            
            st.subheader("🧠 AI Agent Root Cause Analysis")
            st.markdown(report)
            
        except Exception as e:
            st.error(f"Pipeline execution failed: {str(e)}")

# Metadata & Trend History Section
st.divider()
st.subheader("📈 Execution History & Trend Monitoring (Metadata Store)")
history_df = tracker.get_history()

if not history_df.empty:
    st.dataframe(history_df, use_container_width=True)
    if len(history_df) > 1:
        st.line_chart(history_df.set_index('timestamp')['quality_score'])
else:
    st.info("No execution history found yet. Run the pipeline from the sidebar to generate logs.")