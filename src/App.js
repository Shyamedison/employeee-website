// src/App.js
import React, { useState } from 'react';
import EmployeeList from './components/EmployeeList';
import EmployeeForm from './components/EmployeeForm';

const App = () => {
  const [employees, setEmployees] = useState([
    { id: 1, name: 'John Doe', position: 'Manager' },
    { id: 2, name: 'Jane Smith', position: 'Developer' },
  ]);

  const handleDelete = (id) => {
    const updatedEmployees = employees.filter(emp => emp.id !== id);
    setEmployees(updatedEmployees);
  };

  

  return (
    <div className="App">
      <EmployeeList employees={employees} onDelete={handleDelete} />
      <EmployeeForm />
    </div>
  );
};

export default App;

