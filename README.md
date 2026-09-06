# 🤖 Agentic Data Quality & Anomaly Detection System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agentic-data-quality-app-bmu3votp3f5yxv2ytn3agq.streamlit.app)

An automated hybrid data quality pipeline that combines deterministic rule-based validation checks with LLM-driven root cause analysis (powered by Llama 3 via Groq), exposed through an interactive Streamlit dashboard.

## 🚀 Features
- **Rule-Based Engine**: Automatically detects missing values, structural anomalies, out-of-range numeric outliers, and invalid categorical status codes.
- **AI-Powered Root Cause Analysis**: Leverages Groq API (`llama-3.3-70b-versatile`) to evaluate quality reports, interpret anomalies, and provide actionable remediation insights.
- **Interactive Streamlit UI**: Provides real-time metrics, raw dataset previews, structural quality summaries, and on-demand LLM diagnostics.

## 🛠️ Tech Stack
- **Language**: Python
- **Data Manipulation**: Pandas, Pydantic
- **Logging**: Loguru
- **AI/LLM**: Groq API (Llama 3)
- **UI Framework**: Streamlit
- **Configuration**: python-dotenv

## ⚙️ Local Installation & Running

1. Clone the repository:
   ```bash
   git clone [https://github.com/tutarzeliha-ctrl/agentic-data-quality-app.git](https://github.com/tutarzeliha-ctrl/agentic-data-quality-app.git)
   cd agentic-data-quality-app
Install dependencies:

Bash
pip install -r requirements.txt
Set up your Groq API key in your environment or code, then run the Streamlit app:

Bash
streamlit run app.py