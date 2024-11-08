import requests
from bs4 import BeautifulSoup
import json
import os


def download_issuer_codes():
    url = 'https://www.mse.mk/mk/stats/symbolhistory/kmb'

    try:
        # Send the HTTP request
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract issuer codes from dropdown options, ignoring any with numbers
        issuer_codes = [
            option.text.strip()
            for option in soup.find_all('option')
            if not any(char.isdigit() for char in option.text)  # Exclude codes with numbers
        ]

        # Check if any issuer codes were found
        if not issuer_codes:
            print("No issuer codes found on the page.")
            return []

        # Print the issuer codes for testing
        print("Filtered Issuer Codes:", issuer_codes)

        # Save issuer codes to a JSON file for persistence
        save_issuer_codes(issuer_codes)

        return issuer_codes

    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return []


def save_issuer_codes(issuer_codes):
    """Save issuer codes to a JSON file."""
    os.makedirs('data', exist_ok=True)  # Ensure the 'data' directory exists
    file_path = 'data/issuer_codes.json'

    try:
        with open(file_path, 'w') as file:
            json.dump(issuer_codes, file, indent=4)
        print(f"Issuer codes saved to {file_path}")

    except IOError as e:
        print(f"An error occurred while saving issuer codes: {e}")


# Run the function if this file is executed directly
if __name__ == "__main__":
    download_issuer_codes()
