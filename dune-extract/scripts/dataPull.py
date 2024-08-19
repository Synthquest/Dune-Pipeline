import os
from dotenv import load_dotenv
import pandas as pd
from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
from datetime import datetime, timedelta

def get_max_date_from_csv(csv_file):
    try:
        # Load the CSV data into a DataFrame
        df = pd.read_csv(csv_file)
        
        if df.empty:
            # If the DataFrame is empty, return the default date
            print("CSV file is empty. Defaulting to January 1st, 2000.")
            return datetime(2000, 1, 1), df
        
        # Convert the 'date' column to datetime objects
        df['date'] = pd.to_datetime(df['date'])
        
        # Find the maximum date in the 'date' column
        max_date = df['date'].max()
        
        return max_date, df
    except pd.errors.EmptyDataError:
        # Handle the case where the CSV is completely empty
        print("CSV file is completely empty. Defaulting to January 1st, 2000.")
        return datetime(2000, 1, 1), pd.DataFrame()

# Query Date with timestamp:
csv_file = 'query_results.csv'  # Replace with your CSV file path
max_date, df_existing = get_max_date_from_csv(csv_file)
query_date = max_date - timedelta(days=3)
print(f"Query Date: {query_date}")

# Ensure query_date has a timestamp:
query_date = query_date.replace(hour=0, minute=0, second=0, microsecond=0)

# Define your query
query = QueryBase(
    name="watcher_query",
    query_id=3911861,
    params=[
        QueryParameter.date_type(name="date", value=f"{query_date}")
    ],
)

# Load your .env file from the root folder
dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

# Replace 'your_query_id' with the actual query ID you want to export
api_key = os.getenv("DUNE_KEY")

# Set up the Dune client
client = DuneClient(api_key)

# Fetch the results as a DataFrame
try:
    results_df = client.run_query_dataframe(query)
    
    # Append new data to the existing CSV file
    with open(csv_file, 'a') as f:
        results_df.to_csv(f, header=f.tell()==0, index=False)  # Append without header if file exists
    
    # Convert 'date' column in results_df to datetime if needed
    results_df['date'] = pd.to_datetime(results_df['date'])

    # Remove existing data after query_date in df_existing
    df_existing['date'] = pd.to_datetime(df_existing['date'])
    df_existing = df_existing[df_existing['date'] <= query_date]

    # Concatenate df_existing and results_df
    combined_df = pd.concat([df_existing, results_df], ignore_index=True)
    
    # Sort combined_df by the 'date' column
    combined_df = combined_df.sort_values(by='date')

    # Save back to CSV
    combined_df.to_csv(csv_file, index=False)
    
    print("Query results appended and updated successfully.")
except Exception as e:
    print(f"Failed to retrieve or update data: {str(e)}")
