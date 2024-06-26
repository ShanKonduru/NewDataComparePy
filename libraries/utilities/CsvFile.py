import pandas as pd

class CsvFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
