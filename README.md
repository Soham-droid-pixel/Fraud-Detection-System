# 🛡️ Fraud Detection API with Flask

This project is a **Flask-based REST API** that uses a machine learning model to detect fraudulent banking transactions. It integrates with a **MySQL** database to fetch transaction and customer data and predicts fraud based on a trained model.

## 📁 Dataset Source

The model was trained on a publicly available dataset from Kaggle:
🔗 [Transactions Fraud Datasets - Kaggle](https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets)

---

## 📌 Features

* REST API with Flask
* Fraud prediction based on structured transaction and customer data
* Integration with MySQL for fetching transaction records
* Prediction from both JSON input and transaction ID
* Model trained and saved using `fraud detection model.ipynb`

---

## ⚙️ Technologies Used

* Python 3
* Flask
* Scikit-learn
* Pandas
* Joblib
* MySQL (Connector for Python)

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Soham-droid-pixel/fraud-detection-api.git
cd fraud-detection-api
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

> **Note**: Ensure MySQL is installed and configured correctly.

### 4. Prepare MySQL Database

* Create a database named `BankDB`.
* Create `transactions` and `customers` tables based on the structure of your dataset.
* Import the data from the Kaggle dataset.

### 5. Run the Flask App

```bash
python app.py
```

API will run locally at:
📍 `http://127.0.0.1:5000`

---

## 🔍 API Endpoints

### ➤ `POST /predict`

Predicts fraud from direct JSON input.

**Request Body** (sample):

```json
{
  "client_id_x": 1,
  "amount": 123.45,
  "zip": 12345,
  "mcc": 5411,
  "client_id_y": 1,
  "has_chip": "Yes",
  "num_cards_issued": 2,
  "credit_limit": 5000,
  "acct_open_date": "2020-01-01",
  "year_pin_last_changed": 2023,
  "card_type_Credit": 1,
  "card_type_Debit": 0,
  "card_type_Debit_Prepaid": 0,
  "use_chip_Chip_Transaction": 1,
  "use_chip_Online_Transaction": 0,
  "use_chip_Swipe_Transaction": 0,
  "card_on_dark_web_No": 1,
  "transaction_hour": 14,
  "transaction_day": 12,
  "transaction_month": 3,
  "transaction_year": 2023,
  "exp_month": 12,
  "exp_year": 2025
}
```

**Response**:

```json
{
  "is_fraud": 0,
  "fraud_probability": 0.0832,
  "message": "No fraud detected."
}
```

---

### ➤ `GET /predict/<transaction_id>`

Fetches transaction data from the database and returns a fraud prediction.

**Response**:

```json
{
  "transaction_id": "TX12345",
  "is_fraud": 1,
  "fraud_probability": 0.9734,
  "message": "Fraud detected!"
}
```

---

## 📂 File Structure

```
├── app.py                   # Main Flask application
├── model.pkl                # Trained ML model
├── fraud detection model.ipynb   # Jupyter notebook for training
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🧠 Model Details

* Trained using a Gradient Boosting / RandomForest classifier (customizable).
* Used one-hot encoding and feature engineering (date processing, chip usage, etc.).
* The final model is serialized using `joblib`.

---

## 🛠️ To Do

* ✅ Add logging and error tracking
* 🔲 Add authentication (API keys / tokens)
* 🔲 Deploy to cloud (e.g., Heroku, AWS, etc.)
* 🔲 Frontend dashboard for visualizing transactions

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss.

