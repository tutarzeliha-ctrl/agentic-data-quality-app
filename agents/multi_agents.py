import pandas as pd

class ValidatorAgent:
    """Validator Agent: Runs deterministic rule-based checks and detects anomalies."""
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def validate(self) -> dict:
        missing_counts = self.df.isnull().sum().to_dict()
        total_rows = len(self.df)
        invalid_statuses = int((self.df['status'].isin(['INVALID_STATUS', 'UNKNOWN'])).sum()) if 'status' in self.df.columns else 0
        
        return {
            "total_rows": total_rows,
            "missing_values": missing_counts,
            "invalid_status_count": invalid_statuses
        }

class RemediationAgent:
    """Remediation Agent: Suggests automated SQL/Python fixes based on validation findings."""
    def __init__(self, validation_results: dict):
        self.results = validation_results

    def suggest_fixes(self) -> str:
        fixes = []
        if sum(self.results["missing_values"].values()) > 0:
            fixes.append("- **Missing Values Fix:** Run imputation or drop rows with missing critical identifiers using `df.dropna(subset=['customer_id'])` or fill numerical gaps with median values.")
        if self.results["invalid_status_count"] > 0:
            fixes.append(f"- **Data Standardization Fix:** Found {self.results['invalid_status_count']} invalid status records. Execute a cleaning script to map unrecognized statuses to 'PENDING' or 'SUCCESS'.")
        
        if not fixes:
            fixes.append("- **Status:** No critical remediation required. Data is clean.")
            
        return "\n".join(fixes)

class ReporterAgent:
    """Reporter Agent: Summarizes the pipeline execution for management/operations."""
    def __init__(self, quality_score: float, remediation_suggestions: str):
        self.quality_score = quality_score
        self.suggestions = remediation_suggestions

    def generate_executive_report(self) -> str:
        status_label = "🟢 Healthy" if self.quality_score > 90 else "🟡 Needs Attention" if self.quality_score > 75 else "🔴 Critical"
        
        report = f"""
### 📋 Executive Data Quality Summary
* **Overall Pipeline Health Status:** {status_label}
* **Calculated Quality Score:** `{self.quality_score:.2f}%`

#### Recommended Actions:
{self.suggestions}
        """
        return report.strip()