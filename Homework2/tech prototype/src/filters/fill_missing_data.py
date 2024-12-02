from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import json
import os


def format_price_macedonian(price):
    """Format a float price to Macedonian format '1.000,00'."""
    # Format the price as a string with two decimal places and replace separators
    return f"{price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fill_missing_data(issuer_code, last_date):
    # Ignore issuer codes with numbers
    if any(char.isdigit() for char in issuer_code):
        print(f"Ignoring issuer code with numbers: {issuer_code}")
        return

    # Determine the start date for data retrieval
    if last_date is None:
        # Calculate a date 10 years back from today
        start_date = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')
    else:
        # Use the last available date
        start_date = last_date

    # Set the URL for the historical data page
    url = f'https://www.mse.mk/mk/stats/symbolhistory/{issuer_code}'

    try:
        # Send the HTTP request to fetch the data page
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the table that contains the historical data
        table = soup.find('table', {'class': 'table'})

        # Check if the table was found
        if table is None:
            print(f"Table not found on the page for issuer {issuer_code}.")
            return  # Stop if the table is not found

        # Extract rows from the table, skipping the header row
        new_data = []
        for row in table.find_all('tr')[1:]:  # Adjust [1:] if there’s no header
            columns = row.find_all('td')
            if len(columns) >= 2:
                date_text = columns[0].get_text(strip=True)
                price_text = columns[1].get_text(strip=True)

                # Convert date and price, handling any format issues
                try:
                    date = datetime.strptime(date_text, '%d.%m.%Y').strftime('%Y-%m-%d')
                    # Convert price to a float and then to Macedonian format
                    price = format_price_macedonian(float(price_text.replace(',', '').replace('.', '.')))

                    # Only add data within the required date range
                    if date >= start_date:
                        new_data.append({'date': date, 'price': price})

                except ValueError:
                    print(f"Skipping invalid data row: {date_text}, {price_text}")

        # Path to the data file for the given issuer
        data_file = f'data/{issuer_code}.json'

        # Load existing data if it exists, or initialize an empty list
        if os.path.exists(data_file):
            with open(data_file, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Combine new data with existing data, avoiding duplicates
        combined_data = existing_data + new_data

        # Save the combined data back to the JSON file
        with open(data_file, 'w') as file:
            json.dump(combined_data, file, indent=4)

        print(f"Data for {issuer_code} has been updated from {start_date} to today.")

    except requests.RequestException as e:
        print(f"An error occurred while fetching data for {issuer_code}: {e}")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data for {issuer_code}: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
