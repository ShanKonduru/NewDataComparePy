class HtmlReportGenerator:
    def generate_html_report(self, merged_df, stats, dataset_id):
        """Generates an HTML report based on the comparison results and statistics."""
        # Define the background colors based on the _Merge column values
        bg_colors = {
            "Exists in Source and Target": "000000; background: green;",
            "Exists in Source Only": "000000; background: red;",
            "Exists in Target Only": "000000; background: yellow;"
        }

        # Generate the HTML for the detailed differences table with conditional formatting
        detailed_diff_html = "<table>\n"
        detailed_diff_html += "<tr>" + "".join(f"<th>{col}</th>" for col in merged_df.columns) + "</tr>\n"
        
        for _, row in merged_df.iterrows():
            merge_status = row['_merge']
            print(merge_status)
            bg_color = bg_colors.get(merge_status, "")
            print(bg_color)
            detailed_diff_html += f"<tr style='color: #{bg_color}'>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>\n"

        detailed_diff_html += "</table>"

        html = f"""
        <html>
        <head>
            <title>Comparison Report - {dataset_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .header {{ font-size: 24px; margin-bottom: 20px; }}
                .section {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">Comparison Report - {dataset_id}</div>
            <div class="section">
                <h2>Summary</h2>
                <table>
                    <tr><th>Source File Rows</th><td>{stats['src_row_count']}</td></tr>
                    <tr><th>Target File Rows</th><td>{stats['target_row_count']}</td></tr>
                    <tr><th>Matching Records</th><td>{stats['matching_records']}</td></tr>
                    <tr><th>Source Only Records</th><td>{stats['src_only_records']}</td></tr>
                    <tr><th>Target Only Records</th><td>{stats['target_only_records']}</td></tr>
                </table>
            </div>
            <div class="section">
                <h2>Detailed Differences</h2>
                {detailed_diff_html}
            </div>
        </body>
        </html>
        """
        return html
