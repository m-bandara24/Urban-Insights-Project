from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from config import db_config
import bcrypt
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Enable CORS for the app
CORS(app) 

# Connect to MySQL
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None

# Sign Up Route
@app.route('/api/signup', methods=['POST'])
def sign_up():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'All fields are required'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'message': 'Email already exists'}), 409

        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
        conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Error as e:
        print("Database error:", e)
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        cursor.close()
        conn.close()

# Sign In Route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Both email and password are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            token = jwt.encode(
                {'user_id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                app.config['SECRET_KEY'],
                algorithm="HS256"
            )
            return jsonify({'message': 'Login successful', 'token': token}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    finally:
        cursor.close()
        conn.close()

# Token Validation Route
@app.route('/api/validate-token', methods=['POST'])
def validate_token():
    token = request.json.get('token')

    if not token:
        return jsonify({'success':'false','message': 'Token is required'}), 400

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return jsonify({'success':'true','message': 'Token is valid', 'user_id': decoded['user_id']}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'success':'false','message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'success':'false','message': 'Invalid token'}), 401

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
