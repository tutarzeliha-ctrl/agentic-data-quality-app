import os
import json
import pandas as pd
from loguru import logger
from groq import Groq

class DataQualityAgent:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
       
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def load_data(self):
        if os.path.exists(self.data_path):
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Data successfully loaded from {self.data_path}. Total rows: {len(self.df)}")
        else:
            logger.error(f"Data file not found at {self.data_path}")
            raise FileNotFoundError(f"File not found: {self.data_path}")

    def run_rule_based_checks(self) -> dict:
        """Runs initial statistical and structural checks before AI analysis."""
        if self.df is None:
            self.load_data()

        report = {
            "total_rows": len(self.df),
            "missing_values": self.df.isnull().sum().to_dict(),
            "amount_max": float(self.df["amount"].max()),
            "amount_min": float(self.df["amount"].min()),
            "invalid_statuses": list(self.df[~self.df["status"].isin(["SUCCESS", "FAILED", "PENDING"])]["status"].unique())
        }
        
        logger.info("Rule-based data quality checks completed.")
        return report

    def analyze_with_llm(self, quality_report: dict) -> str:
        """Sends the quality report to the LLM for intelligent anomaly evaluation."""
        prompt = f"""
        You are an expert Data Quality Engineer. Analyze the following data quality report summary 
        and provide insights, potential root causes for the anomalies, and recommended remediation steps.

        Report Summary:
        {json.dumps(quality_report, indent=2)}

        Provide your response in a clear, professional technical format with actionable suggestions.
        """

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            logger.info("LLM data quality analysis successfully generated.")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Failed to generate LLM analysis: {e}")
            return f"Error during LLM analysis: {str(e)}"

if __name__ == "__main__":
    agent = DataQualityAgent("config/sample_transactions.csv")
    quality_report = agent.run_rule_based_checks()
    ai_insights = agent.analyze_with_llm(quality_report)
    print("\n--- AI Data Quality Insights ---")
    print(ai_insights)