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