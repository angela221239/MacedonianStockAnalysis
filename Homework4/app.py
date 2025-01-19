from flask import Flask, render_template, request, redirect, url_for
from main import main
from filters.check_latest_data import check_latest_data
from filters.fill_missing_data import fill_missing_data
from factory import AnalysisFactory
import os
import json

app = Flask(__name__)

# Path to JSON data
DATA_PATH = os.path.join("data", "issuer_codes.json")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "password":
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        # Normally, save to DB or file
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/run_pipeline', methods=['GET'])
def run_pipeline():
    try:
        main()  # Run the full pipeline
        return render_template('run_pipeline.html', message="Pipeline executed successfully!")
    except Exception as e:
        return render_template('run_pipeline.html', message=f"Error occurred: {str(e)}")


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
                return render_template('process_issuer.html',
                                       message=f"Fetched data for {issuer_code} for the last 10 years.")
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


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    with open(DATA_PATH, 'r') as file:
        data = json.load(file)
    filtered_data = data
    if request.method == 'POST':
        issuer_code = request.form.get('issuer_code')
        if issuer_code:
            filtered_data = {issuer_code: data[issuer_code]} if issuer_code in data else {}
    return render_template('dashboard.html', data=filtered_data)


if __name__ == "__main__":
    app.run(debug=True)
