import os
import json
from datetime import datetime


def check_latest_data(issuer_code):
    """
    Checks the latest available date of data for a given issuer.

    Parameters:
        issuer_code (str): The code of the issuer to check.

    Returns:
        tuple: ("Data Found", latest_date) if data exists,
               ("No Data", None) if the file is missing,
               ("Corrupted Data", None) if the file is corrupted.
    """
    # Path to the data file for the given issuer code
    data_file = f'data/{issuer_code}.json'

    # Check if the data file exists
    if not os.path.exists(data_file):
        return "No Data", None  # Signal to download 10 years of data

    try:
        # Load the data from the JSON file
        with open(data_file, 'r') as file:
            data = json.load(file)

        # Ensure data is a list of dictionaries
        if not isinstance(data, list):
            print(f"Unexpected data format in {data_file}: Expected a list of entries.")
            return "Corrupted Data", None

        # Find the latest date in the data entries
        latest_date = max(
            datetime.strptime(entry['date'], '%Y-%m-%d')
            for entry in data if 'date' in entry
        ).strftime('%Y-%m-%d')

        return "Data Found", latest_date

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        # Handle potential errors in reading or parsing the JSON file
        print(f"Error reading {data_file}: {e}")
        return "Corrupted Data", None
