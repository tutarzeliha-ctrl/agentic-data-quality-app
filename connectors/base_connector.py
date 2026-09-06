import os
import pandas as pd
from loguru import logger

class DataConnector:
    def __init__(self, source_type: str, path_or_query: str):
        self.source_type = source_type
        self.path_or_query = path_or_query

    def load_data(self) -> pd.DataFrame:
        if self.source_type == "csv":
            if os.path.exists(self.path_or_query):
                df = pd.read_csv(self.path_or_query)
                logger.info(f"Data successfully loaded from CSV path: {self.path_or_query}")
                return df
            else:
                logger.error(f"CSV file not found at {self.path_or_query}")
                raise FileNotFoundError(f"File not found: {self.path_or_query}")
        
        elif self.source_type == "bigquery":
            
            logger.info("BigQuery connector placeholder called.")
            raise NotImplementedError("BigQuery connector will be implemented in the next phase.")
        
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")