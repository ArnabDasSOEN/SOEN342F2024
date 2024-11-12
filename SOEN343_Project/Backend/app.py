# app.py
"""
This module initializes the Flask application, sets up configurations,
and registers blueprints for the application routes.
"""
import os
from flask import Flask, request, jsonify, session
from dbconnection import db  # Import db from extensions
# Import the blueprint registration function
from Models.Customer_Interaction.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from blueprints import register_blueprints
from config import Config, TestConfig

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object(TestConfig)
else:
    app.config.from_object(Config)


db.init_app(app)  # Initialize db with app

with app.app_context():
    db.drop_all()
    db.create_all()  # This creates all tables


@app.route('/')
def home():
    if 'user_id' in session:
        return jsonify({'message': 'You are signed in'}), 200
    return jsonify({'message': 'You are not signed in'}), 200

app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    session['user_id'] = user.id
    
    return jsonify({'message': 'Successfully signed in'}), 200

app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

app.route('/signout')
def signout():
    session.clear()
    return jsonify({'message': 'Successfully signed out'}), 200


# Register all blueprints from the central function
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)
