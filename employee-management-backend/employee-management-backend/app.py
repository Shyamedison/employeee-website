from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    department = db.Column(db.String(100))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    employee_list = [{"id": e.id, "name": e.name, "age": e.age, "department": e.department} for e in employees]
    return jsonify(employee_list)

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    new_employee = Employee(name=data['name'], age=data['age'], department=data['department'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message": "Employee added successfully!"})

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()
    employee = Employee.query.get(id)
    if employee:
        employee.name = data['name']
        employee.age = data['age']
        employee.department = data['department']
        db.session.commit()
        return jsonify({"message": "Employee updated successfully!"})
    return jsonify({"message": "Employee not found"}), 404

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "Employee deleted successfully!"})
    return jsonify({"message": "Employee not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
