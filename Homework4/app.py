from flask import Flask, render_template, request, redirect, url_for
import os
import json

# Flask app setup
app = Flask(__name__)

# Define the path to the users.json file
USERS_FILE = os.path.join("credentials", "users.json")


# Ensure the data folder exists
os.makedirs("data", exist_ok=True)


@app.route('/')
def index():
    # Redirect to the login page
    return redirect(url_for('login'))


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        users = load_users()

        if username in users:
            return render_template('signup.html', error="Username already exists. Please choose another.")

        users[username] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password
        }

        save_users(users)
        return redirect(url_for('login'))

    return render_template('signup.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()

        if username in users and users[username]['password'] == password:
            return redirect(url_for('dashboard', username=username))

        return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')


# Dashboard route
@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = request.args.get('username')  # Retrieve the username from query parameters

    # Load user information
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            users = json.load(file)
    else:
        users = {}

    user = users.get(username, {"first_name": "Guest", "last_name": ""})

    # Example data for the dashboard
    data_folder = os.path.join("data")
    latest_data = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".json"):
            issuer = os.path.splitext(filename)[0]
            with open(os.path.join(data_folder, filename), 'r') as file:
                records = json.load(file)
                if records:
                    latest_record = records[-1]
                    latest_data.append({
                        #"issuer": issuer,
                        #"date": latest_record.get("date", "N/A"),
                        #"close": latest_record.get("close", "N/A"),
                        #"volume": latest_record.get("volume", "N/A")
                    })

    return render_template('dashboard.html', user=user, data=latest_data)


@app.route('/run_pipeline', methods=['GET'])
def run_pipeline():
    try:
        # Placeholder for running the main pipeline
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
            # Placeholder for processing an issuer
            return render_template('process_issuer.html', message=f"Processed data for issuer {issuer_code}.")
        except Exception as e:
            return render_template('process_issuer.html', message=f"Error: {str(e)}")
    return render_template('process_issuer.html')


def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: users.json is empty or corrupted. Resetting file.")
            return {}  # Return an empty dictionary if the file is invalid
    return {}  # Return an empty dictionary if the file doesn't exist


def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)


if __name__ == "__main__":
    app.run(debug=True)
