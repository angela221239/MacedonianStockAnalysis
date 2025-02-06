from flask import Flask, render_template, request
from lstm_prediction import preprocess_data, train_xgb_model, predict_future_prices, load_stock_data
from technical_analysis import perform_technical_analysis
from fundamental_analysis import analyze_sentiment

# Tell Flask where to find templates
app = Flask(__name__, template_folder="templates")


# **Home Page (User Interface)**
@app.route('/')
def home():
    return render_template('home.html')


# **Process User Input from the Web Form**
@app.route('/process_request', methods=['POST'])
def process_request():
    try:
        issuer_code = request.form.get('issuer_code')
        analysis_type = request.form.get('analysis_type')
        text_input = request.form.get('text_input', '')

        if not issuer_code:
            return render_template('result.html', error="Issuer code is required!")

        if analysis_type == "technical":
            data = load_stock_data(issuer_code)
            result_data = perform_technical_analysis(data).to_dict(orient='records')

        elif analysis_type == "fundamental":
            if not text_input:
                return render_template('result.html', error="Text input is required for Fundamental Analysis!")
            result_data = analyze_sentiment(text_input)

        elif analysis_type == "lstm":
            data = load_stock_data(issuer_code)
            X_train, X_test, y_train, y_test, scaler = preprocess_data(data)
            model = train_xgb_model(X_train, y_train)
            recent_data = scaler.transform(data[['Close']].values)
            result_data = predict_future_prices(model, recent_data, scaler, steps=10).tolist()

        else:
            return render_template('result.html', error="Invalid analysis type selected!")

        return render_template('result.html', result=result_data)

    except Exception as e:
        return render_template('result.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
