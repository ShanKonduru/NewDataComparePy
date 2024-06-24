from ExcelFile import ExcelFile
from  DataComparator import DataComparator

class ExcelDataComparator(DataComparator):
    def __init__(self, source_file_path, target_file_path, sheet_name):
        super().__init__()
        self.source_excel = ExcelFile(source_file_path, sheet_name)
        self.target_excel = ExcelFile(target_file_path, sheet_name)
    
    def compare_excel_with_excel(self, src_query, dest_query):
        """Compares two Excel files using SQL query and returns rows that are different."""
        return self.compare_data(self.source_excel.data, self.target_excel.data, src_query, dest_query)
