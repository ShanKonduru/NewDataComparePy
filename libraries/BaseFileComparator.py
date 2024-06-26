import pandas as pd
from pandasql import sqldf
from libraries.utilities.HTMLReportGenerator import HtmlReportGenerator

class FileComparator:
    def __init__(self):
        self.html_report_generator = HtmlReportGenerator()
    
    def execute_sql_query(self, df, query):
        """Executes SQL query on a DataFrame using pandasql."""
        return sqldf(query, locals())
    
    def get_query_columns(self, query):
        """Extracts column names from the SQL query."""
        select_part = query.split('FROM')[0]
        columns = select_part.replace('SELECT', '').split(',')
        columns = [col.split('as')[1].strip() if 'as' in col else col.strip() for col in columns]
        return columns
    
    def compare_data(self, source_data, target_data, src_query, dest_query):
        """Compares two DataFrames using SQL queries and returns rows that are different."""
        stats = {
            "src_row_count": 0,
            "target_row_count": 0,
            "matching_records": 0,
            "src_only_records": 0,
            "target_only_records": 0
        }
        try:
            # Execute SQL queries on source and target data
            source_data = self.execute_sql_query(source_data, src_query)
            target_data = self.execute_sql_query(target_data, dest_query)
            
            # Get the columns used in the SQL queries for comparison
            src_columns = self.get_query_columns(src_query)
            dest_columns = self.get_query_columns(dest_query)
            
            if set(src_columns) != set(dest_columns):
                raise ValueError("Source and Target queries do not select the same columns")
            
            # Compare DataFrames using the common columns
            merged_df = pd.merge(source_data, target_data, on=src_columns, how='outer', indicator=True)
            
            # Map the _merge column values
            merge_mapping = {
                'both': 'Exists in Source and Target',
                'left_only': 'Exists in Source Only',
                'right_only': 'Exists in Target Only'
            }
            merged_df['_merge'] = merged_df['_merge'].map(merge_mapping)
            
            # Populate stats
            stats = {
                "src_row_count": len(source_data),
                "target_row_count": len(target_data),
                "matching_records": len(merged_df[merged_df['_merge'] == 'Exists in Source and Target']),
                "src_only_records": len(merged_df[merged_df['_merge'] == 'Exists in Source Only']),
                "target_only_records": len(merged_df[merged_df['_merge'] == 'Exists in Target Only'])
            }
            
            return merged_df, stats
        
        except Exception as e:
            print(f"Error during comparison: {e}")
            return pd.DataFrame(), stats  # Return an empty DataFrame and stats or handle error as appropriate
    
    def generate_html_report(self, merged_df, stats, dataset_id):
        """Generates an HTML report based on the comparison results and statistics."""
        print(f"Generating HTML report for dataset {dataset_id} with stats: {stats}")
        return self.html_report_generator.generate_html_report(merged_df, stats, dataset_id)
