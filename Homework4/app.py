from flask import Flask, render_template, request, redirect, url_for

# Initialize Flask app
app = Flask(__name__)

# Temporary storage for user credentials (for demo purposes)
users = {
    "admin": {"email": "admin@example.com", "password": "password"}
}


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate user credentials
        if username in users and users[username]['password'] == password:
            return redirect(url_for('dashboard'))

        # Invalid credentials
        return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        if username in users:
            return render_template('signup.html', error="Username already exists. Please choose another.")

        # Save user data
        users[username] = {'email': email, 'password': password}
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    # Example stock data
    stock_data = [
        {"Date": "2024-12-01", "Close": 100, "SMA_20": 98, "EMA_20": 99, "RSI_14": 45},
        {"Date": "2024-12-02", "Close": 102, "SMA_20": 99, "EMA_20": 100, "RSI_14": 50},
        {"Date": "2024-12-03", "Close": 104, "SMA_20": 100, "EMA_20": 101, "RSI_14": 55},
    ]
    return render_template('dashboard.html', stock_data=stock_data)


if __name__ == '__main__':
    app.run(debug=True)
