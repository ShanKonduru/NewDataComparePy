import pandas as pd
from  DataComparator import DataComparator

class CSVDataComparator(DataComparator):
    def __init__(self, source_file_path, target_file_path):
        super().__init__()
        self.source_csv = pd.read_csv(source_file_path)
        self.target_csv = pd.read_csv(target_file_path)
    
    def compare_csv_with_csv(self, src_query, dest_query):
        """Compares two CSV files using SQL query and returns rows that are different."""
        return self.compare_data(self.source_csv, self.target_csv, src_query, dest_query)
