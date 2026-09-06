import streamlit as st
import pandas as pd
import os
from connectors.base_connector import DataConnector
from metadata.tracker import MetadataTracker
from agents.multi_agents import ValidatorAgent, RemediationAgent, ReporterAgent
from utils.slack_alert import send_slack_alert

st.set_page_config(
    page_title="Agentic Data Quality Platform",
    page_icon="🤖",
    layout="wide"
)

# Initialize Metadata Tracker
tracker = MetadataTracker()

# Base directory for absolute path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.title("🤖 Enterprise Agentic Data Quality & Anomaly Detection")
st.markdown("Automated hybrid data quality pipeline combining multi-agent validation with metadata tracking and alerts.")

# Sidebar Controls
st.sidebar.header("Pipeline Configuration")
source_option = st.sidebar.selectbox("Select Data Source", ["Local CSV", "Custom Upload"])

data_path = os.path.join(BASE_DIR, "sample_data.csv")
if source_option == "Custom Upload":
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        data_path = os.path.join(BASE_DIR, "uploaded_temp.csv")
        with open(data_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

st.sidebar.markdown("---")
st.sidebar.header("Notifications")
slack_webhook = st.sidebar.text_input("Slack Webhook URL (Optional)", type="password")

# Run Quality Check Button
if st.sidebar.button("Run Quality Pipeline & AI Analysis", type="primary"):
    with st.spinner("Executing multi-agent pipeline and validating dataset..."):
        try:
            # 1. Load Data via Connector
            connector = DataConnector("csv", data_path)
            df = connector.load_data()
            
            # 2. Run Multi-Agent Architecture
            validator = ValidatorAgent(df)
            validation_metrics = validator.validate()
            
            remediator = RemediationAgent(validation_metrics)
            remediation_fixes = remediator.suggest_fixes()
            
            # 3. Calculate metrics for logging
            total_rows = validation_metrics["total_rows"]
            missing_vals = int(sum(validation_metrics["missing_values"].values()))
            invalid_status = validation_metrics["invalid_status_count"]
            
            # Quality score heuristic
            quality_score = max(0.0, 100.0 - ((missing_vals + invalid_status) / (total_rows * max(1, len(df.columns))) * 100))
            
            # 4. Generate Executive Report via Reporter Agent
            reporter = ReporterAgent(quality_score, remediation_fixes)
            report = reporter.generate_executive_report()
            
            # 5. Log to Metadata Store
            tracker.log_run(total_rows, missing_vals, invalid_status, quality_score)
            
            # 6. Send Slack Alert if Webhook is Provided
            if slack_webhook:
                alert_sent = send_slack_alert(slack_webhook, quality_score, total_rows, missing_vals)
                if alert_sent:
                    st.sidebar.success("Slack alert sent successfully!")
            
            st.success("Multi-agent pipeline executed successfully and logged!")
            
            # Display Results
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Rows", total_rows)
            col2.metric("Missing Values", missing_vals)
            col3.metric("Calculated Quality Score", f"{quality_score:.2f}%")
            
            st.subheader("📊 Dataset Preview")
            st.dataframe(df.head(10))
            
            st.subheader("🧠 Multi-Agent Executive Report")
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