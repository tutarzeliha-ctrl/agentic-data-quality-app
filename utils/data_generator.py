import pandas as pd
import numpy as np

def generate_sample_data(num_rows=1000):
    np.random.seed(42)
    data = {
        "transaction_id": [f"TXN_{i:05d}" for i in range(num_rows)],
        "customer_id": np.random.randint(1000, 5000, size=num_rows),
        "amount": np.random.exponential(scale=50.0, size=num_rows),
        "transaction_date": pd.date_range(start="2026-09-01", periods=num_rows, freq="min"),
        "status": np.random.choice(["SUCCESS", "FAILED", "PENDING", "UNKNOWN"], size=num_rows, p=[0.85, 0.1, 0.04, 0.01])
    }
    
    df = pd.DataFrame(data)
    
    # Inject deliberate data quality issues (anomalies) for testing
    df.loc[10:15, "amount"] = np.nan  # Missing values
    df.loc[50, "amount"] = 99999.0     # Extreme amount anomaly
    df.loc[100:105, "status"] = "INVALID_STATUS" # Invalid categorical state
    
    return df

if __name__ == "__main__":
    df = generate_sample_data()
    df.to_csv("config/sample_transactions.csv", index=False)
    print("Sample dataset successfully generated and saved.")