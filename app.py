from flask import Flask, render_template, request
from utils.db_connection import create_connection
from config import Config
import hashlib

app = Flask(__name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Fetch form data
        first_name = request.form['firstName']
        # [add remaining fields here...]

        # Connect to database and insert user
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Users (FirstName, ...) VALUES (?, ...)",
            (first_name, ...)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return "Registration successful!"

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
