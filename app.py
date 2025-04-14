from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create database and table if not exists
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS loan_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            income REAL,
            loan_amount REAL,
            cibil_score INTEGER,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Loan Eligibility Checker
@app.route('/loan-eligibility', methods=['GET', 'POST'])
def loan_eligibility():
    result = None
    if request.method == 'POST':
        income = float(request.form['income'])
        loan_amount = float(request.form['loan_amount'])
        cibil_score = int(request.form['cibil_score'])

        if income >= 20000 and loan_amount <= income * 20 and cibil_score >= 650:
            result = "Eligible ✅ - Apply for the best loan offer now!"
        else:
            result = "Not Eligible ❌ - Improve your profile and try again."

        # Save the query to database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO loan_queries (income, loan_amount, cibil_score, result) VALUES (?, ?, ?, ?)',
                  (income, loan_amount, cibil_score, result))
        conn.commit()
        conn.close()

    return render_template('loan_eligibility.html', result=result)

# Credit Score Improvement Guide
@app.route('/credit-score-tips')
def credit_score_tips():
    return render_template('credit_score_tips.html')

# Free Calculators
@app.route('/calculators', methods=['GET', 'POST'])
def calculators():
    emi_result = None
    if request.method == 'POST':
        principal = float(request.form['principal'])
        annual_rate = float(request.form['annual_rate'])
        tenure_years = int(request.form['tenure_years'])

        monthly_rate = annual_rate / (12 * 100)
        months = tenure_years * 12
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        emi_result = round(emi, 2)

    return render_template('calculators.html', emi_result=emi_result)

if __name__ == '__main__':
    app.run(debug=True)
