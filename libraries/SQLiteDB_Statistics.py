import numpy as np
import pandas as pd
from .SQLiteDB import SQLiteDB

class SQLiteDB_Statistics:
    def __init__(self, db_path):
        self.db = SQLiteDB(db_path)
    
    def get_summary_statistics(self, table_name):
        """Fetch summary statistics (min, Q1, median, mode, Q3, max, std dev) for a table."""
        query = f"SELECT * FROM {table_name};"
        df = self.db.fetch_query(query)

        # Compute statistics
        stats = {}
        for column in df.select_dtypes(include=np.number).columns:
            stats[column] = {
                'min': df[column].min(),
                'Q1': df[column].quantile(0.25),
                'median': df[column].median(),
                'mode': df[column].mode()[0] if not df[column].mode().empty else np.nan,
                'Q3': df[column].quantile(0.75),
                'max': df[column].max(),
                'std_dev': df[column].std()
            }
        return stats

    def get_tables(self):
        """Fetch all table names from the database."""
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables_df = self.db.fetch_query(query)
        return tables_df['name'].tolist()