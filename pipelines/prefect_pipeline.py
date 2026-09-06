import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ["PREFECT_ANALYTICS_ENABLED"] = "false"

import pandas as pd
from prefect import flow, task
from connectors.base_connector import DataConnector
from agents.multi_agents import ValidatorAgent, RemediationAgent, ReporterAgent
from metadata.tracker import MetadataTracker

@task(name="Load Dataset Task")
def load_data_task(data_path: str) -> pd.DataFrame:
    connector = DataConnector("csv", data_path)
    return connector.load_data()

@task(name="Multi-Agent Validation Task")
def validate_data_task(df: pd.DataFrame) -> dict:
    validator = ValidatorAgent(df)
    return validator.validate()

@task(name="Remediation & Logging Task")
def process_and_log_task(validation_metrics: dict, df: pd.DataFrame):
    remediator = RemediationAgent(validation_metrics)
    fixes = remediator.suggest_fixes()
    
    total_rows = validation_metrics["total_rows"]
    missing_vals = int(sum(validation_metrics["missing_values"].values()))
    invalid_status = validation_metrics["invalid_status_count"]
    
    quality_score = max(0.0, 100.0 - ((missing_vals + invalid_status) / (total_rows * max(1, len(df.columns))) * 100))
    
    reporter = ReporterAgent(quality_score, fixes)
    report = reporter.generate_executive_report()
    
    tracker = MetadataTracker()
    tracker.log_run(total_rows, missing_vals, invalid_status, quality_score)
    
    return quality_score, report

@flow(name="Enterprise Data Quality Flow")
def data_quality_flow(data_path: str):
    df = load_data_task(data_path)
    metrics = validate_data_task(df)
    score, report = process_and_log_task(metrics, df)
    return score, report

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "sample_data.csv")
    print(f"Looking for dataset at: {path}")
    data_quality_flow(path)