from flask import Flask, request, jsonify
import sqlite3
import bcrypt

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    phoneNumber = data.get('phoneNumber')
    email = data.get('email')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO customers (username, password, phoneNumber, email)
        VALUES (?, ?, ?, ?)
    ''', (username, hashed_password, phoneNumber, email))

    connection.commit()
    connection.close()

    return jsonify({'message': 'User added successfully'}), 201

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    user_record = cursor.fetchone()
    connection.close()

    if user_record and bcrypt.checkpw(password.encode('utf-8'), user_record[0]):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


if __name__ == '__main__':
    app.run(debug=True)
