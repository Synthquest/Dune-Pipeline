import pandas as pd
from datetime import datetime, timedelta

def get_max_date_from_csv(csv_file):
    # Load the CSV data into a DataFrame
    df = pd.read_csv(csv_file)

    # Convert the 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])

    # Find the maximum date in the 'date' column
    max_date = df['date'].max()

    return max_date

# Example usage:
csv_file = 'query_results.csv'  # Replace with your CSV file path
max_date = get_max_date_from_csv(csv_file)
query_date = max_date - timedelta(days=3)
print(f"Maximum Date from CSV: {max_date}")
print(f"{query_date}")