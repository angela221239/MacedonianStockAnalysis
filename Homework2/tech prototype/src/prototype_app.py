from flask import Flask, render_template, request
from main import main
from filters.check_latest_data import check_latest_data
from filters.fill_missing_data import fill_missing_data


# Your app code follows...

app = Flask(__name__)

# Root route: Render the homepage
@app.route('/')
def home():
    return render_template('home.html')

# Run pipeline route
@app.route('/run_pipeline', methods=['GET'])
def run_pipeline():
    try:
        main()
        return render_template('run_pipeline.html', message="Pipeline executed successfully!")
    except Exception as e:
        return render_template('run_pipeline.html', message=f"Error occurred: {str(e)}")

# Process issuer route
@app.route('/process_issuer', methods=['GET', 'POST'])
def process_issuer():
    if request.method == 'POST':
        issuer_code = request.form.get('issuer_code')
        if not issuer_code:
            return render_template('process_issuer.html', message="Issuer code not provided!")
        try:
            status, latest_date = check_latest_data(issuer_code)
            if status == "No Data":
                fill_missing_data(issuer_code, None)
                return render_template('process_issuer.html', message=f"Fetched data for the last 10 years for {issuer_code}.")
            elif status == "Data Found":
                fill_missing_data(issuer_code, latest_date)
                return render_template('process_issuer.html', message=f"Fetched missing data for {issuer_code}.")
            elif status == "Corrupted Data":
                return render_template('process_issuer.html', message=f"Data is corrupted for {issuer_code}.")
            else:
                return render_template('process_issuer.html', message="Unexpected status.")
        except Exception as e:
            return render_template('process_issuer.html', message=f"Error: {str(e)}")
    return render_template('process_issuer.html')

if __name__ == "__main__":
    app.run(debug=True)
