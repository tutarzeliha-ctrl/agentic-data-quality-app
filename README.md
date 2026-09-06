Markdown
# 🚀 Enterprise Agentic Data Quality & Anomaly Detection Platform

An automated, hybrid data quality pipeline combining multi-agent architecture, workflow orchestration, metadata tracking, and real-time alerting. Built with Python, Streamlit, Prefect, and SQLite.

🔗 **Live App Demo:** [Streamlit Cloud Application](https://agentic-data-quality-app-bmu3votp3f5yxv2ytn3agq.streamlit.app)

---

## 🏗️ Architecture & Core Components

The platform is designed with a modular, decoupled structure to ensure high maintainability and scalability:

* **`connectors/`**: Handles flexible data ingestion (supports local CSVs and extensible to cloud warehouses).
* **`agents/`**: Multi-agent framework containing:
  * **Validator Agent**: Runs deterministic rule-based checks and anomaly detection.
  * **Remediation Agent**: Automatically suggests SQL/Python fixes based on data anomalies.
  * **Reporter Agent**: Generates executive summaries and system health metrics.
* **`metadata/`**: SQLite-backed metadata tracker logging execution history, missing values, error counts, and quality scores.
* **`pipelines/`**: Prefect-orchestrated background workflows ensuring robust task execution and error handling.
* **`app.py`**: Interactive Streamlit user interface providing real-time pipeline triggers, visual monitoring, and Slack alert integrations.

---

## 📊 Key Features

* **Multi-Agent Validation**: Automated anomaly detection tracking missing values and status corruptions.
* **Smart Remediation**: Context-aware suggestions for data cleansing and imputation.
* **Workflow Orchestration**: Built-in Prefect tasks and flows for enterprise-grade execution tracking.
* **Metadata Store & Trend Monitoring**: Persistent tracking of pipeline health history over time.
* **Automated Alerting**: Real-time webhook notifications dispatched directly to Slack channels.

---

## ⚙️ Quick Start & Local Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tutarzeliha-ctrl/agentic-data-quality-app.git](https://github.com/tutarzeliha-ctrl/agentic-data-quality-app.git)
   cd agentic-data-quality-app
Install dependencies:

Bash
pip install -r requirements.txt
Generate sample dataset:

Bash
python utils/data_generator.py
Launch the Streamlit UI:

Bash
streamlit run app.py
Run the Prefect Pipeline (CLI):

Bash
python pipelines/prefect_pipeline.py
🖼️ Platform Preview
🛠️ Tech Stack
Frontend/UI: Streamlit

Orchestration: Prefect

Processing & Logic: Pandas, Python

Metadata & Storage: SQLite

Alerts: Slack Webhooks