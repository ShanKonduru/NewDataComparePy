import time
import datetime
import os

class PerformanceMetrics:
    def __init__(self):
        self.tracking_data = {}

    def start_tracking(self, process_name):
        if process_name in self.tracking_data:
            print(f"Warning: Process '{process_name}' is already being tracked.")
        self.tracking_data[process_name] = {'start_time': time.time(), 'end_time': None}

    def end_tracking(self, process_name):
        if process_name not in self.tracking_data:
            print(f"Error: Process '{process_name}' was not started.")
            return
        if self.tracking_data[process_name]['end_time'] is not None:
            print(f"Warning: Process '{process_name}' has already ended.")
            return
        self.tracking_data[process_name]['end_time'] = time.time()
        self._print_duration(process_name)

    def _print_duration(self, process_name):
        start_time = self.tracking_data[process_name]['start_time']
        end_time = self.tracking_data[process_name]['end_time']
        if start_time and end_time:
            duration = end_time - start_time
            print(f"Process '{process_name}' ran for {duration:.4f} seconds.")
        else:
            print(f"Could not calculate duration for process '{process_name}'.")

    def get_duration(self, process_name):
        if process_name not in self.tracking_data:
            print(f"Error: Process '{process_name}' does not exist.")
            return None
        if self.tracking_data[process_name]['end_time'] is None:
            print(f"Warning: Process '{process_name}' has not ended yet.")
            return None
        return self.tracking_data[process_name]['end_time'] - self.tracking_data[process_name]['start_time']

    def generate_html_report(self, output_folder='./output-reports', prefix='perf_report'):
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Generate timestamp for the file name
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        # Construct the file name
        file_name = f"{prefix}_{timestamp}.html"
        file_path = os.path.join(output_folder, file_name)

        # Generate the HTML content
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                table, th, td {{
                    border: 1px solid #000;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                .header {{
                    margin-bottom: 20px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 12px;
                    text-align: center;
                }}
            </style>
            <title>Performance Report</title>
        </head>
        <body>
            <div class="header">
                <h1>Performance Report</h1>
                <p>Generated on: {generation_time}</p>
            </div>
            <table>
                <tr>
                    <th>Process Name</th>
                    <th>Start Time</th>
                    <th>End Time</th>
                    <th>Duration (seconds)</th>
                </tr>
        """.format(generation_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        for process_name, times in self.tracking_data.items():
            start_time = times['start_time']
            end_time = times['end_time']
            duration = end_time - start_time if end_time else None
            html_content += """
                <tr>
                    <td>{process_name}</td>
                    <td>{start_time}</td>
                    <td>{end_time}</td>
                    <td>{duration:.4f}</td>
                </tr>
            """.format(
                process_name=process_name,
                start_time=datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S') if start_time else 'N/A',
                end_time=datetime.datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S') if end_time else 'N/A',
                duration=duration if duration else 0
            )

        html_content += """
            </table>
            <div class="footer">
                <p>&copy; {year} Performance Metrics Report</p>
            </div>
        </body>
        </html>
        """.format(year=datetime.datetime.now().year)

        # Write the HTML content to file
        with open(file_path, 'w') as file:
            file.write(html_content)

        print(f"Performance report generated: {file_path}")
