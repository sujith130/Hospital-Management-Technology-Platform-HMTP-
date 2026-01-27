import os
import zipfile

# Define the project structure and file contents
project_name = "frontend_phase6"

files = {
    # --- CONFIG ---
    "src/config/navConfig.js": """
export const navItems = {
  admin: [
    { label: 'Overview', path: '/dashboard', icon: '📊' },
    { label: 'Manage Users', path: '/dashboard/users', icon: '👥' },
    { label: 'System Settings', path: '/dashboard/settings', icon: '⚙️' },
    { label: 'Pharmacy', path: '/dashboard/inventory', icon: '📦' },
  ],
  doctor: [
    { label: 'My Schedule', path: '/dashboard/schedule', icon: '📅' },
    { label: 'Patients', path: '/dashboard/patients', icon: '🩺' },
    { label: 'Appointments', path: '/dashboard/appointments', icon: '📋' },
  ],
  patient: [
    { label: 'My Health', path: '/dashboard/overview', icon: '❤️' },
    { label: 'Prescriptions', path: '/dashboard/prescriptions', icon: '💊' },
    { label: 'Billing', path: '/dashboard/billing', icon: '💳' },
  ]
};
""",

    # --- SERVICES ---
    "src/services/api.js": """
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api/v1', 
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // localStorage.removeItem('token'); 
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
""",

    # --- CONTEXT ---
    "src/context/AuthContext.jsx": """
import React, { createContext, useState, useEffect, useContext } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('token');
      const savedUser = localStorage.getItem('user');
      if (token && savedUser) {
        setUser(JSON.parse(savedUser));
      }
      setLoading(false);
    };
    loadUser();
  }, []);

  const login = async (email, password) => {
    try {
      // Mocking response for demo if backend isn't running
      // const response = await api.post('/auth/login', { email, password });
      
      // MOCK LOGIC START (Remove in production)
      const mockUser = { name: 'Test User', email, role: 'doctor' }; // Change role to test others
      const mockToken = '12345';
      localStorage.setItem('token', mockToken);
      localStorage.setItem('user', JSON.stringify(mockUser));
      setUser(mockUser);
      return { success: true };
      // MOCK LOGIC END

    } catch (error) {
      return { success: false, message: error.response?.data?.message || "Login failed" };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
""",

    # --- COMPONENTS ---
    "src/components/ProtectedRoute.jsx": """
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ allowedRoles }) => {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
""",

    "src/components/DashboardLayout.jsx": """
import React from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { navItems } from '../config/navConfig';
import '../styles/Dashboard.css';

const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  if (!user) return null;
  const menu = navItems[user.role] || [];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="sidebar-header">MediCare App</div>
        <ul className="nav-links">
          {menu.map((item) => (
            <li key={item.path}>
              <NavLink 
                to={item.path} 
                className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}
              >
                <span className="nav-icon">{item.icon}</span>
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </aside>
      <main className="main-content">
        <header className="top-header">
          <h3>{user.role.charAt(0).toUpperCase() + user.role.slice(1)} Dashboard</h3>
          <div className="user-info">
            <span>Hello, <strong>{user.name || user.email}</strong></span>
            <button onClick={handleLogout} className="logout-btn">Logout</button>
          </div>
        </header>
        <div className="page-content">
          <Outlet /> 
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
""",

    # --- PAGES ---
    "src/pages/Login.jsx": """
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Auth.css';

const Login = () => {
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [formData, setFormData] = useState({ email: '', password: '', name: '', role: 'patient' });
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (isLoginMode) {
      const result = await login(formData.email, formData.password);
      if (result.success) navigate('/dashboard'); 
      else setError(result.message);
    } else {
      alert('Registration successful! Please log in.');
      setIsLoginMode(true);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2 className="auth-title">{isLoginMode ? 'Welcome Back' : 'Create Account'}</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          {!isLoginMode && (
            <div className="form-group">
              <label>Full Name</label>
              <input type="text" name="name" className="form-input" value={formData.name} onChange={handleChange} required />
            </div>
          )}
          <div className="form-group">
            <label>Email Address</label>
            <input type="email" name="email" className="form-input" value={formData.email} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input type="password" name="password" className="form-input" value={formData.password} onChange={handleChange} required />
          </div>
          {!isLoginMode && (
            <div className="form-group">
              <label>I am a...</label>
              <select name="role" className="form-input" value={formData.role} onChange={handleChange}>
                <option value="patient">Patient</option>
                <option value="doctor">Doctor</option>
                <option value="admin">Administrator</option>
              </select>
            </div>
          )}
          <button type="submit" className="btn-primary">{isLoginMode ? 'Login' : 'Register'}</button>
        </form>
        <p className="toggle-text">
          {isLoginMode ? "Don't have an account?" : "Already have an account?"}
          <span className="toggle-link" onClick={() => setIsLoginMode(!isLoginMode)}>{isLoginMode ? 'Register here' : 'Login here'}</span>
        </p>
      </div>
    </div>
  );
};

export default Login;
""",

    "src/pages/Patients.jsx": """
import React, { useState, useEffect } from 'react';
import api from '../services/api';
import '../styles/Table.css';

const Patients = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [newPatient, setNewPatient] = useState({ firstName: '', lastName: '', email: '', phone: '', dob: '' });

  useEffect(() => {
    // Mock Data
    setPatients([
      { id: 1, firstName: 'John', lastName: 'Doe', email: 'john@example.com', phone: '555-1234', dob: '1990-01-01' },
      { id: 2, firstName: 'Jane', lastName: 'Smith', email: 'jane@example.com', phone: '555-5678', dob: '1985-05-12' }
    ]);
    setLoading(false);
  }, []);

  const handleAddSubmit = (e) => {
    e.preventDefault();
    setPatients([...patients, { ...newPatient, id: Date.now() }]);
    setShowAddForm(false);
  };

  const filteredPatients = patients.filter(p => 
    p.firstName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.phone.includes(searchTerm)
  );

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
            <input placeholder="First Name" className="form-input" value={newPatient.firstName} onChange={e => setNewPatient({...newPatient, firstName: e.target.value})} required />
            <input placeholder="Last Name" className="form-input" value={newPatient.lastName} onChange={e => setNewPatient({...newPatient, lastName: e.target.value})} required />
            <input placeholder="Email" className="form-input" value={newPatient.email} onChange={e => setNewPatient({...newPatient, email: e.target.value})} />
            <input placeholder="Phone" className="form-input" value={newPatient.phone} onChange={e => setNewPatient({...newPatient, phone: e.target.value})} required />
            <input type="date" className="form-input" value={newPatient.dob} onChange={e => setNewPatient({...newPatient, dob: e.target.value})} required />
            <button type="submit" className="btn-primary" style={{ gridColumn: 'span 2' }}>Save Patient</button>
          </form>
        </div>
      )}
      <input type="text" placeholder="Search..." className="search-bar" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} style={{ marginBottom: '15px' }} />
      <div className="data-table-container">
        <table className="data-table">
          <thead><tr><th>Name</th><th>Contact</th><th>DOB</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            {filteredPatients.map((patient) => (
              <tr key={patient.id}>
                <td>{patient.firstName} {patient.lastName}</td>
                <td>{patient.phone}<br/><small>{patient.email}</small></td>
                <td>{patient.dob}</td>
                <td><span className="status-badge status-active">Active</span></td>
                <td><button className="btn-sm">View</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Patients;
""",

    "src/pages/DoctorSchedule.jsx": """
import React, { useState, useEffect } from 'react';
import '../styles/Schedule.css';

const DoctorSchedule = () => {
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState(null);

  useEffect(() => {
    const times = ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00', '17:00'];
    setSlots(times.map(time => ({ id: time, time, status: 'available' })));
  }, [selectedDate]);

  const handleSlotClick = (slot) => {
    if (slot.status === 'booked') return;
    setSelectedSlot(slot);
  };

  const confirmBooking = () => {
    setSlots(slots.map(s => s.time === selectedSlot.time ? { ...s, status: 'booked', patientName: 'John Doe' } : s));
    setSelectedSlot(null);
    alert("Booked!");
  };

  return (
    <div className="schedule-container">
      <div className="date-header"><h3>{selectedDate}</h3></div>
      <div className="slots-grid">
        {slots.map((slot) => (
          <div key={slot.time} className={`time-slot ${slot.status === 'available' ? 'slot-available' : 'slot-booked'}`} onClick={() => handleSlotClick(slot)}>
            <span className="time-label">{slot.time}</span>
            <span className="slot-status">{slot.status}</span>
          </div>
        ))}
      </div>
      {selectedSlot && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Book {selectedSlot.time}</h3>
            <button className="btn-primary" onClick={confirmBooking}>Confirm</button>
            <button className="btn-sm" onClick={() => setSelectedSlot(null)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DoctorSchedule;
""",

    "src/pages/Inventory.jsx": """
import React from 'react';
import '../styles/Table.css';

const Inventory = () => {
  const medicines = [
    { id: 1, name: 'Paracetamol 500mg', batch: 'B101', stock: 150, expiry: '2026-12-01', price: 5.00 },
    { id: 2, name: 'Amoxicillin 250mg', batch: 'B102', stock: 8, expiry: '2025-08-15', price: 12.50 },
  ];

  return (
    <div>
      <div className="page-header"><h2>Pharmacy Inventory</h2><button className="btn-add">+ Add Medicine</button></div>
      <div className="data-table-container">
        <table className="data-table">
          <thead><tr><th>Name</th><th>Batch</th><th>Expiry</th><th>Stock</th><th>Price</th></tr></thead>
          <tbody>
            {medicines.map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td><td>{item.batch}</td><td>{item.expiry}</td>
                <td><span className={`status-badge ${item.stock < 10 ? 'status-inactive' : 'status-active'}`} style={item.stock < 10 ? {color: 'red'} : {}}>{item.stock}</span></td>
                <td>${item.price.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
export default Inventory;
""",

    "src/pages/Billing.jsx": """
import React, { useState } from 'react';
import '../styles/Billing.css';
import '../styles/Table.css';

const Billing = () => {
  const [cart, setCart] = useState([]);
  const items = [{ id: 1, name: 'Consultation Fee', price: 50.00 }, { id: 2, name: 'Paracetamol', price: 5.00 }];
  
  const addToCart = (item) => setCart([...cart, item]);
  const total = cart.reduce((acc, item) => acc + item.price, 0).toFixed(2);

  return (
    <div className="billing-container">
      <div className="billing-card">
        <h3>Add Items</h3>
        {items.map(i => <button key={i.id} className="btn-sm" onClick={() => addToCart(i)}>{i.name} (${i.price})</button>)}
      </div>
      <div className="billing-card">
        <div className="invoice-header"><h4>Invoice</h4></div>
        <ul className="invoice-item-list">{cart.map((i, idx) => <li key={idx} className="invoice-item"><span>{i.name}</span><span>${i.price}</span></li>)}</ul>
        <div className="invoice-total">Total: ${total}</div>
      </div>
    </div>
  );
};
export default Billing;
""",

    # --- STYLES ---
    "src/styles/Auth.css": """
.auth-container { display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f5; }
.auth-card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
.auth-title { margin-bottom: 1.5rem; color: #333; }
.form-group { margin-bottom: 1rem; text-align: left; }
.form-input { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
.btn-primary { width: 100%; padding: 0.75rem; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; margin-top: 1rem; }
.toggle-text { margin-top: 1rem; font-size: 0.9rem; color: #666; }
.toggle-link { color: #007bff; cursor: pointer; text-decoration: underline; margin-left: 5px; }
""",

    "src/styles/Dashboard.css": """
.dashboard-container { display: flex; height: 100vh; width: 100vw; background-color: #f4f6f9; }
.sidebar { width: 250px; background-color: #2c3e50; color: white; display: flex; flex-direction: column; flex-shrink: 0; }
.sidebar-header { padding: 1.5rem; font-size: 1.25rem; font-weight: bold; border-bottom: 1px solid #34495e; }
.nav-links { list-style: none; padding: 0; margin-top: 1rem; }
.nav-item { display: flex; align-items: center; padding: 1rem 1.5rem; color: #bdc3c7; text-decoration: none; cursor: pointer; }
.nav-item:hover, .nav-item.active { background-color: #34495e; color: white; }
.nav-icon { margin-right: 10px; }
.main-content { flex-grow: 1; display: flex; flex-direction: column; overflow: hidden; }
.top-header { height: 60px; background: white; border-bottom: 1px solid #e1e4e8; display: flex; justify-content: space-between; align-items: center; padding: 0 2rem; }
.page-content { padding: 2rem; overflow-y: auto; height: 100%; }
.user-info { display: flex; gap: 10px; align-items: center; }
.logout-btn { border: 1px solid red; color: red; background: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; }
""",

    "src/styles/Table.css": """
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.search-bar { padding: 10px; width: 300px; border: 1px solid #ddd; border-radius: 4px; }
.data-table-container { background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th, .data-table td { padding: 15px; border-bottom: 1px solid #e9ecef; }
.data-table th { background-color: #f8f9fa; font-weight: 600; }
.status-badge { padding: 4px 8px; border-radius: 12px; font-size: 0.85rem; font-weight: 500; }
.status-active { background-color: #d4edda; color: #155724; }
.status-inactive { background-color: #e2e3e5; color: #383d41; }
.btn-add { background-color: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
.btn-sm { padding: 5px 10px; font-size: 0.8rem; margin-right: 5px; cursor: pointer; border: 1px solid #ddd; background: white; border-radius: 3px; }
""",

    "src/styles/Schedule.css": """
.schedule-container { display: flex; flex-direction: column; gap: 20px; }
.date-header { display: flex; justify-content: center; background: white; padding: 15px; border-radius: 8px; }
.slots-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px; }
.time-slot { background: white; border: 1px solid #e1e4e8; border-radius: 8px; padding: 20px; text-align: center; cursor: pointer; }
.slot-available { border-left: 5px solid #28a745; }
.slot-booked { border-left: 5px solid #dc3545; background-color: #fff5f5; cursor: default; }
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; }
.modal-content { background: white; padding: 25px; border-radius: 8px; width: 400px; display: flex; flex-direction: column; gap: 10px; }
""",

    "src/styles/Billing.css": """
.billing-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: calc(100vh - 150px); }
.billing-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); display: flex; flex-direction: column; }
.invoice-header { border-bottom: 2px dashed #ddd; padding-bottom: 15px; margin-bottom: 15px; text-align: center; }
.invoice-total { margin-top: auto; font-size: 1.5rem; font-weight: bold; text-align: right; border-top: 2px solid #333; padding-top: 15px; }
.invoice-item-list { list-style: none; padding: 0; flex-grow: 1; }
.invoice-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }
""",

    # --- ROOT ---
    "src/App.js": """
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import DashboardLayout from './components/DashboardLayout';
import Login from './pages/Login';
import Patients from './pages/Patients';
import DoctorSchedule from './pages/DoctorSchedule';
import Inventory from './pages/Inventory';
import Billing from './pages/Billing';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Navigate to="/login" replace />} />
          
          <Route element={<ProtectedRoute />}>
             <Route path="/dashboard" element={<DashboardLayout />}>
                <Route index element={<div>Welcome to your Dashboard</div>} />
                <Route path="patients" element={<Patients />} />
                <Route path="schedule" element={<DoctorSchedule />} />
                <Route path="inventory" element={<Inventory />} />
                <Route path="billing" element={<Billing />} />
             </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
""",
    
    "package.json": """
{
  "name": "frontend_phase6",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "axios": "^1.6.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
"""
}

# Create directory structure and files
if not os.path.exists(project_name):
    os.makedirs(project_name)

for filepath, content in files.items():
    full_path = os.path.join(project_name, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip())

# Create Zip
zip_filename = f"{project_name}.zip"
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_name):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, os.path.dirname(project_name))
            zipf.write(file_path, arcname)

print(f"✅ Success! Created '{project_name}' folder and '{zip_filename}'")