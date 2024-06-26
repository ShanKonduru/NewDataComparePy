import pandas as pd
from libraries.utilities.ExcelFile import ExcelFile
from libraries.BaseFileComparator import FileComparator
from libraries.utilities.Consts import StringConstants

class CrossFileComparator(FileComparator):
    def __init__(self, source_format, source_file_path, target_format, target_file_path, sheet_name=None):
        super().__init__()
        self.source_format = source_format
        self.target_format = target_format
        
        # Load source data based on format
        if source_format == StringConstants.CSV:
            self.source_data = pd.read_csv(source_file_path)
            print(f"Loaded source CSV data:\n{self.source_data.head()}")
        elif source_format == StringConstants.XLSX:
            self.source_data = ExcelFile(source_file_path, sheet_name).data
            if isinstance(self.source_data, pd.DataFrame):
                print(f"Loaded source Excel data:\n{self.source_data.head()}")
            else:
                print(f"Error: source data is not a DataFrame. Data type: {type(self.source_data)}")
        else:
            raise ValueError(f"Unsupported source format: {source_format}")
        
        # Load target data based on format
        if target_format == StringConstants.CSV:
            self.target_data = pd.read_csv(target_file_path)
            print(f"Loaded target CSV data:\n{self.target_data.head()}")
        elif target_format == StringConstants.XLSX:
            self.target_data = ExcelFile(target_file_path, sheet_name).data
            if isinstance(self.target_data, pd.DataFrame):
                print(f"Loaded target Excel data:\n{self.target_data.head()}")
            else:
                print(f"Error: target data is not a DataFrame. Data type: {type(self.target_data)}")
        else:
            raise ValueError(f"Unsupported target format: {target_format}")
    
    def compare_csv_with_xlsx(self, src_query, dest_query):
        """Compares CSV data with Excel data using SQL queries."""
        print("Comparing CSV with Excel...")
        return self.compare_data(self.source_data, self.target_data, src_query, dest_query)
    
    def compare_xlsx_with_csv(self, src_query, dest_query):
        """Compares Excel data with CSV data using SQL queries."""
        print("Comparing Excel with CSV...")
        return self.compare_data(self.source_data, self.target_data, src_query, dest_query)
