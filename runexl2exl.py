import pandas as pd
from pandasql import sqldf
from ExcelFile import ExcelFile
from ConfigLoader import ConfigLoader
from ExcelDataComparator import ExcelDataComparator
from CsvDataComparator import CSVDataComparator
from HTMLReportGenerator import HtmlReportGenerator
from PerformanceMetrics import PerformanceMetrics
from CrossDataComparator import CrossDataComparator

if __name__ == "__main__":
    # Load configuration from JSON file
    config_loader = ConfigLoader('config.json')
    
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

        if config.get('ignore', 'No').lower() == 'yes':
            print(f"Skipping dataset {config['id']} as it is marked to be ignored.")
            continue
        
        source_file_path = config["source_file_path"]
        target_file_path = config["target_file_path"]
        sheet_name = config["sheet_name"]
        src_query = config["src_query"]
        dest_query = config["dest_query"]
        
        if source_file_path.endswith('.xlsx') and target_file_path.endswith('.xlsx'):
            data_comparator = ExcelDataComparator(source_file_path, target_file_path, sheet_name)
            merged_df, stats = data_comparator.compare_excel_with_excel(src_query, dest_query)
        elif source_file_path.endswith('.csv') and target_file_path.endswith('.csv'):
            data_comparator = CSVDataComparator(source_file_path, target_file_path)
            merged_df, stats = data_comparator.compare_csv_with_csv(src_query, dest_query)
        elif source_file_path.endswith('.csv') and target_file_path.endswith('.xlsx'):
            data_comparator = CrossDataComparator("CSV", source_file_path, "XLSX", target_file_path, sheet_name)
            merged_df, stats = data_comparator.compare_csv_with_xlsx(src_query, dest_query)
        elif source_file_path.endswith('.xlsx') and target_file_path.endswith('.csv'):
            data_comparator = CrossDataComparator("XLSX", source_file_path, "CSV", target_file_path, sheet_name)
            merged_df, stats = data_comparator.compare_xlsx_with_csv(src_query, dest_query)
        else:
            print(f"Unsupported file types for dataset {dataset_id}")
            continue

        # Generate HTML report
        html_report = data_comparator.generate_html_report(merged_df, stats, dataset_id)
        
        # Save the HTML report to a file
        report_file_path = f"./output-reports/report_{dataset_id}.html"
        with open(report_file_path, "w") as file:
            file.write(html_report)
        
        print(f"Report for dataset {dataset_id} saved to {report_file_path}")
        metrics.end_tracking(dataset_id)
    
    metrics.generate_html_report()
