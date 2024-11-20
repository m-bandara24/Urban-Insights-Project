from flask import Flask, request, jsonify,render_template, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from config import db_config
import bcrypt
import jwt
import datetime
from flask_mail import Mail, Message
import random



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Enable CORS for the app
CORS(app) 

# Mail configuration
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '5eab03e0f38f45'
app.config['MAIL_PASSWORD'] = '78f93eb49d73b5'

mail = Mail(app)

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

# forget password - verify email, send email with a code

@app.route('/api/send-reset-email', methods=['POST'])
def send_reset_email():
    data = request.json
    email = data.get('email')

    # Verify email exists in the database
    # conn = sqlite3.connect('users.db') 
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM user WHERE email=?", (email,))
    # user = cursor.fetchone()
    # conn.close()

    # if not user:
    #     return jsonify({"message": "Email not found!"}), 404

    # Generate reset token (random code for simplicity)
    reset_token = random.randint(100000, 999999)

    # Save the reset token in the database
    # conn = sqlite3.connect('users.db') 
    # cursor = conn.cursor()
    # cursor.execute("UPDATE user SET reset_token=? WHERE email=?", (reset_token, email))
    # conn.commit()
    # conn.close()

    # Send email
    try:
        msg = Message("Password Reset Request", sender="urbaninsight123@gmail.com", recipients=[email])
        msg.body = f"Use this code to reset your password: {reset_token}"
        mail.send(msg)
        return jsonify({"message": "Reset email sent!"}), 200
    except Exception as e:
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500

# forget password - reset password
@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    reset_token = data.get('token')
    new_password = data.get('new_password')

    # Verify the reset token
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND reset_token=?", (email, reset_token))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"message": "Invalid token or email!"}), 400

    # Update the password
    cursor.execute("UPDATE users SET password=?, reset_token=NULL WHERE email=?", (new_password, email))
    conn.commit()
    conn.close()

    return jsonify({"message": "Password reset successfully!"}), 200

# FOrgot password web page
@app.route('/forget')
def forget():
    return render_template('forgotpassword.html')

# Reset_password web page
@app.route('/reset')
def reset():
    return render_template('reset_password.html')


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
