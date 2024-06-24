import pandas as pd

class ExcelFile:
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.data = self._load_excel()

    def _load_excel(self):
        try:
            df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            return df
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error
