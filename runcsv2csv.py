from ConfigLoader import ConfigLoader
import ExcelDataComparator
from CsvDataComparator import CSVDataComparator

import json

if __name__ == "__main__":
    config_loader = ConfigLoader('config.json')
    datasets = config_loader.get_all_dataset_names()
    
    for dataset in datasets:
        dataset_id = dataset['id']
        source_file_path = dataset['source_file_path']
        target_file_path = dataset['target_file_path']
        sheet_name = dataset.get('sheet_name')  # Use get() to handle the absence of sheet_name in non-Excel files
        src_query = dataset['src_query']
        dest_query = dataset['dest_query']
        
        if source_file_path.endswith('.xlsx') and target_file_path.endswith('.xlsx'):
            comparator = ExcelDataComparator(source_file_path, target_file_path, sheet_name)
        elif source_file_path.endswith('.csv') and target_file_path.endswith('.csv'):
            comparator = CSVDataComparator(source_file_path, target_file_path)
        else:
            print(f"Unsupported file types for dataset {dataset_id}")
            continue
        
        merged_df, stats = comparator.compare_excel_with_excel(src_query, dest_query)
        html_report = comparator.generate_html_report(merged_df, stats, dataset_id)
        
        # Save the HTML report
        report_file = f'./output-reports/report_{dataset_id}.html'
        with open(report_file, 'w') as f:
            f.write(html_report)
        print(f"Report generated for {dataset_id}: {report_file}")
