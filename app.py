from flask import Flask, request, jsonify
import joblib
import pandas as pd
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Load the fraud detection model
model = joblib.load('model.pkl')

# MySQL database connection
db_config = {
    'host': 'localhost',
    'user': 'root',          # Change if different
    'password': '',          # Change if you have a password
    'database': 'BankDB'
}

# Expected features for the model
FEATURES = [
    'client_id_x', 'amount', 'zip', 'mcc', 'client_id_y', 'has_chip',
    'num_cards_issued', 'credit_limit', 'acct_open_date', 'year_pin_last_changed',
    'card_type_Credit', 'card_type_Debit', 'card_type_Debit_Prepaid',
    'use_chip_Chip_Transaction', 'use_chip_Online_Transaction', 'use_chip_Swipe_Transaction',
    'card_on_dark_web_No', 'transaction_hour', 'transaction_day', 'transaction_month',
    'transaction_year', 'exp_month', 'exp_year'
]

def preprocess(data):
    """Preprocesses input data for the model."""
    df = pd.DataFrame([data])

    # Convert 'acct_open_date' to days since account opening
    if 'acct_open_date' in df.columns:
        try:
            df['acct_open_date'] = pd.to_datetime(df['acct_open_date'])
            df['acct_open_date'] = (pd.Timestamp.now() - df['acct_open_date']).dt.days
        except Exception as e:
            raise ValueError(f"Invalid 'acct_open_date': {e}")
    else:
        df['acct_open_date'] = 0

    # Convert 'has_chip' from Yes/No to 1/0
    df['has_chip'] = df.get('has_chip', 'No').map({'Yes': 1, 'No': 0})

    # Fill missing features with 0
    for feature in FEATURES:
        if feature not in df.columns:
            df[feature] = 0

    # Ensure numeric data types
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    return df[FEATURES]  # Ensure this return is **inside** the function

def fetch_transaction(transaction_id):
    """Fetches transaction data from the database."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM transactions WHERE transaction_id = %s
        """, (transaction_id,))
        transaction = cursor.fetchone()

        if not transaction:
            return None

        cursor.execute("""
            SELECT * FROM customers WHERE client_id = %s
        """, (transaction['client_id'],))
        customer = cursor.fetchone()

        cursor.close()
        conn.close()

        # Combine transaction and customer data
        if customer:
            transaction.update(customer)
        return transaction

    except mysql.connector.Error as err:
        raise Exception(f"MySQL Error: {err}")

@app.route('/predict', methods=['POST'])
def predict():
    """Predicts fraud from JSON input."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        processed_data = preprocess(data)
        prediction = model.predict(processed_data)[0]
        fraud_probability = model.predict_proba(processed_data)[0][1]

        return jsonify({
            'is_fraud': int(prediction),
            'fraud_probability': round(fraud_probability, 4),
            'message': 'Fraud detected!' if prediction else 'No fraud detected.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict/<transaction_id>', methods=['GET'])
def predict_from_db(transaction_id):
    """Fetches transaction from DB and predicts fraud."""
    try:
        transaction_data = fetch_transaction(transaction_id)
        if not transaction_data:
            return jsonify({'error': f'Transaction {transaction_id} not found.'}), 404

        processed_data = preprocess(transaction_data)
        prediction = model.predict(processed_data)[0]
        fraud_probability = model.predict_proba(processed_data)[0][1]

        return jsonify({
            'transaction_id': transaction_id,
            'is_fraud': int(prediction),
            'fraud_probability': round(fraud_probability, 4),
            'message': 'Fraud detected!' if prediction else 'No fraud detected.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
