from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    position = db.Column(db.String(100), nullable=False)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/employees', methods=['GET'])
@jwt_required()
def get_employees():
    employees = Employee.query.all()
    result = [
        {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "position": employee.position
        } for employee in employees
    ]
    return jsonify(result), 200

@app.route('/api/employees', methods=['POST'])
@jwt_required()
def add_employee():
    data = request.get_json()
    new_employee = Employee(name=data['name'], email=data['email'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message": "Employee added successfully"}), 201

@app.route('/api/employees/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted successfully"}), 200

if __name__ == "__main__":
    app.run(port=5000)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

