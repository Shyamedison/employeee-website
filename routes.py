from app import app, db, bcrypt, jwt
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import Employee, User

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/employees', methods=['GET'])
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

@app.route('/employees', methods=['POST'])
@jwt_required()
def add_employee():
    data = request.get_json()
    new_employee = Employee(name=data['name'], email=data['email'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message": "Employee added successfully"}), 201

@app.route('/employees/<int:id>', methods=['PUT'])
@jwt_required()
def update_employee(id):
    data = request.get_json()
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404
    employee.name = data['name']
    employee.email = data['email']
    employee.position = data['position']
    db.session.commit()
    return jsonify({"message": "Employee updated successfully"}), 200

@app.route('/employees/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted successfully"}), 200
