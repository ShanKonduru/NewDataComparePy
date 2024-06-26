import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from pandasql import sqldf
from libraries.utilities.ExcelFile import ExcelFile
from libraries.utilities.ConfigLoader import ConfigLoader
from libraries.ExcelFileComparator import ExcelFileComparator
from libraries.CsvFileComparator import CSVFileComparator
from libraries.utilities.HTMLReportGenerator import HtmlReportGenerator
from libraries.utilities.PerformanceMetrics import PerformanceMetrics
from libraries.utilities.Consts import StringConstants
from libraries.CrossFileComparator import CrossFileComparator


if __name__ == "__main__":
    # Load configuration from JSON file
    config_loader = ConfigLoader(StringConstants.FILE_CONFIG_NAME )
    
    # Get all dataset names (IDs)
    dataset_ids = config_loader.get_all_dataset_names()
    metrics = PerformanceMetrics()

    for dataset_id in dataset_ids:
        print(f"Processing dataset: {dataset_id}")
        metrics.start_tracking(dataset_id)

        try:
            # Get the configuration for the specified dataset
            config = config_loader.get_config_by_id(dataset_id)
        except ValueError as e:
            print(e)
            continue  # Skip to the next dataset

        if config.get(StringConstants.IGNORE, StringConstants.NO).lower() == StringConstants.YES.lower():
            print(f"Skipping dataset {config[StringConstants.ID]} as it is marked to be ignored.")
            continue
        
        source_file_path = config[StringConstants.SOURCE_FILE_PATH]
        target_file_path = config[StringConstants.TARGET_FILE_PATH]
        sheet_name = config[StringConstants.SHEET_NAME]
        src_query = config[StringConstants.SRC_QUERY]
        dest_query = config[StringConstants.DEST_QUERY]
        
        if source_file_path.endswith(StringConstants.XLSX_EXT.lower()) and target_file_path.endswith(StringConstants.XLSX_EXT.lower()):
            data_comparator = ExcelFileComparator(source_file_path, target_file_path, sheet_name)
            merged_df, stats = data_comparator.compare_excel_with_excel(src_query, dest_query)
        elif source_file_path.endswith(StringConstants.CSV_EXT.lower()) and target_file_path.endswith(StringConstants.CSV_EXT.lower()):
            data_comparator = CSVFileComparator(source_file_path, target_file_path)
            merged_df, stats = data_comparator.compare_csv_with_csv(src_query, dest_query)
        elif source_file_path.endswith(StringConstants.CSV_EXT.lower()) and target_file_path.endswith(StringConstants.XLSX_EXT.lower()):
            data_comparator = CrossFileComparator(StringConstants.CSV, source_file_path, StringConstants.XLSX, target_file_path, sheet_name)
            merged_df, stats = data_comparator.compare_csv_with_xlsx(src_query, dest_query)
        elif source_file_path.endswith(StringConstants.XLSX_EXT.lower()) and target_file_path.endswith(StringConstants.CSV_EXT.lower()):
            data_comparator = CrossFileComparator(StringConstants.XLSX, source_file_path, StringConstants.CSV, target_file_path, sheet_name)
            merged_df, stats = data_comparator.compare_xlsx_with_csv(src_query, dest_query)
        else:
            print(f"Unsupported file types for dataset {dataset_id}")
            continue

        # Generate HTML report
        html_report = data_comparator.generate_html_report(merged_df, stats, dataset_id)
        
        # Save the HTML report to a file
        report_folder = StringConstants.OUTPUT_REPORTS
        report_file_path = f"./{report_folder}/report_{dataset_id}.html"
        with open(report_file_path, "w") as file:
            file.write(html_report)
        
        print(f"Report for dataset {dataset_id} saved to {report_file_path}")
        metrics.end_tracking(dataset_id)
    
    metrics.generate_html_report()
