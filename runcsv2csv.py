from ConfigLoader import ConfigLoader
import ExcelDataComparator
from CsvDataComparator import CSVDataComparator
from Consts import StringConstants

import json

if __name__ == "__main__":
    config_loader = ConfigLoader(StringConstants.JSON_CONFIG_FILE_NAME)
    datasets = config_loader.get_all_dataset_names()
    
    for dataset in datasets:
        dataset_id = dataset[StringConstants.ID]
        source_file_path = dataset[StringConstants.SOURCE_FILE_PATH]
        target_file_path = dataset[StringConstants.TARGET_FILE_PATH]
        sheet_name = dataset.get(StringConstants.SHEET_NAME)  # Use get() to handle the absence of sheet_name in non-Excel files
        src_query = dataset[StringConstants.SRC_QUERY]
        dest_query = dataset[StringConstants.DEST_QUERY]
        
        if source_file_path.endswith(StringConstants.XLSX_EXT.lower()) and target_file_path.endswith(StringConstants.XLSX_EXT.lower()):
            comparator = ExcelDataComparator(source_file_path, target_file_path, sheet_name)
        elif source_file_path.endswith(StringConstants.CSV_EXT.lower()) and target_file_path.endswith(StringConstants.CSV_EXT.lower()):
            comparator = CSVDataComparator(source_file_path, target_file_path)
        else:
            print(f"Unsupported file types for dataset {dataset_id}")
            continue
        
        merged_df, stats = comparator.compare_excel_with_excel(src_query, dest_query)
        html_report = comparator.generate_html_report(merged_df, stats, dataset_id)
        
        # Save the HTML report
        report_folder = StringConstants.OUTPUT_REPORTS
        report_file = f'./{report_folder}/report_{dataset_id}.html'
        with open(report_file, 'w') as f:
            f.write(html_report)
        print(f"Report generated for {dataset_id}: {report_file}")
