import os
from dotenv import load_dotenv
import pandas as pd
from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
from datetime import datetime, timedelta

# Query Date with timestamp:
query_date = datetime(2023, 1, 1)  # Example date to query

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
    
    # Ensure 'date' column in results_df is datetime
    results_df['date'] = pd.to_datetime(results_df['date'])

    # Sort by 'date' column if needed
    results_df = results_df.sort_values(by='date')

    # Save results to CSV file, replacing existing content
    results_df.to_csv('query_results.csv', index=False)
    
    print("Query results replaced successfully.")
except Exception as e:
    print(f"Failed to retrieve or update data: {str(e)}")
