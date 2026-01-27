import React, { useState, useEffect } from 'react';
import api from '../services/api';
import '../styles/Table.css';

const Patients = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [newPatient, setNewPatient] = useState({ first_name: '', last_name: '', gender: 'Male', date_of_birth: '' });

  const fetchPatients = async () => {
    try {
      const res = await api.get('/patients/');
      setPatients(res.data);
    } catch (error) {
      console.error("Fetch Error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  const handleAddSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/patients/', newPatient);
      setShowAddForm(false);
      fetchPatients();
      setNewPatient({ first_name: '', last_name: '', gender: 'Male', date_of_birth: '' });
    } catch (error) {
      alert("Failed to save patient: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  const filteredPatients = patients.filter(p =>
    `${p.first_name} ${p.last_name}`.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) return <div>Loading records...</div>;

  return (
    <div>
      <div className="page-header">
        <h2>Patient Management</h2>
        <button className="btn-add" onClick={() => setShowAddForm(!showAddForm)}>{showAddForm ? 'Cancel' : '+ New Patient'}</button>
      </div>
      {showAddForm && (
        <div style={{ marginBottom: '20px', padding: '20px', background: 'white', borderRadius: '8px' }}>
          <h4>Register New Patient</h4>
          <form onSubmit={handleAddSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
            <input placeholder="First Name" className="form-input" value={newPatient.first_name} onChange={e => setNewPatient({ ...newPatient, first_name: e.target.value })} required />
            <input placeholder="Last Name" className="form-input" value={newPatient.last_name} onChange={e => setNewPatient({ ...newPatient, last_name: e.target.value })} required />
            <select className="form-input" value={newPatient.gender} onChange={e => setNewPatient({ ...newPatient, gender: e.target.value })}>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
            <input type="date" className="form-input" value={newPatient.date_of_birth} onChange={e => setNewPatient({ ...newPatient, date_of_birth: e.target.value })} required />
            <button type="submit" className="btn-primary" style={{ gridColumn: 'span 2' }}>Save Patient</button>
          </form>
        </div>
      )}
      <input type="text" placeholder="Search by name..." className="search-bar" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} style={{ marginBottom: '15px' }} />
      <div className="data-table-container">
        <table className="data-table">
          <thead><tr><th>Name</th><th>Gender</th><th>DOB</th><th>Hospital ID</th><th>Actions</th></tr></thead>
          <tbody>
            {filteredPatients.map((patient) => (
              <tr key={patient.id}>
                <td>{patient.first_name} {patient.last_name}</td>
                <td>{patient.gender}</td>
                <td>{patient.date_of_birth}</td>
                <td><small>{patient.hospital_id}</small></td>
                <td><button className="btn-sm">View History</button></td>
              </tr>
            ))}
            {filteredPatients.length === 0 && <tr><td colSpan="5" style={{ textAlign: 'center' }}>No records found</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Patients;