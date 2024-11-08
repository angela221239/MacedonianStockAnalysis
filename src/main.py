import time
from filters.download_data import download_issuer_codes
from filters.check_latest_data import check_latest_data
from filters.fill_missing_data import fill_missing_data


def main():
    # Step 1: Download issuer codes
    issuer_codes = download_issuer_codes()
    if not issuer_codes:
        print("No issuer codes found. Exiting the pipeline.")
        return

    # Step 2: For each issuer code, check the latest data and fill missing data
    for issuer_code in issuer_codes:
        print(f"\nProcessing data for issuer: {issuer_code}")

        # Check the latest date available in the data file
        status, latest_date = check_latest_data(issuer_code)

        if status == "No Data":
            print(f"No existing data found for {issuer_code}. Downloading data for the last 10 years.")
            fill_missing_data(issuer_code, None)

        elif status == "Data Found":
            print(f"Latest data available for {issuer_code} is dated: {latest_date}")
            print(f"Fetching any missing data up to the current date.")
            fill_missing_data(issuer_code, latest_date)

        elif status == "Corrupted Data":
            print(f"Data file for {issuer_code} is corrupted. Please check and fix the file before proceeding.")

        else:
            print(f"Unexpected status for {issuer_code}: {status}")


if __name__ == "__main__":

    # Start timer
    start_time = time.time()

    main()

    # End timer
    end_time = time.time()

    # Calculate and print the elapsed time
    elapsed_time = end_time - start_time
    print(f"\nPipeline completed in {elapsed_time:.2f} seconds.")
