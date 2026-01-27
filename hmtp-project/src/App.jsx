import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { AuthProvider } from './context/AuthContext';
import MainLayout from './components/layout/MainLayout';

// Pages
import PatientDashboard from './pages/patient/PatientDashboard';
import DoctorDashboard from './pages/doctor/DoctorDashboard';
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminInventory from './pages/admin/AdminInventory';
import LandingPage from './pages/public/LandingPage';

const theme = createTheme({
  palette: {
    primary: { main: '#0288d1' }, // Professional Blue
    secondary: { main: '#ed6c02' }, // Alert Orange
    background: { default: '#f4f6f8' },
  },
  typography: { fontFamily: 'Inter, sans-serif' },
  components: {
    MuiPaper: { styleOverrides: { root: { borderRadius: 12, boxShadow: '0px 4px 20px rgba(0,0,0,0.05)' } } },
    MuiButton: { styleOverrides: { root: { borderRadius: 8, textTransform: 'none', fontWeight: 600 } } },
  },
});

export default function App() {
  return (
    <AuthProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Routes>
             {/* Public Route - No Layout */}
             <Route path="/welcome" element={<LandingPage />} />
             
             {/* Protected Routes - With Layout */}
             <Route path="/*" element={
                <MainLayout>
                  <Routes>
                    <Route path="/" element={<Navigate to="/doctor/dashboard" replace />} />
                    
                    <Route path="/patient/*" element={<Routes>
                      <Route path="dashboard" element={<PatientDashboard />} />
                      <Route path="appointments" element={<PatientDashboard />} /> 
                    </Routes>} />

                    <Route path="/doctor/*" element={<Routes>
                      <Route path="dashboard" element={<DoctorDashboard />} />
                      <Route path="schedule" element={<DoctorDashboard />} /> 
                    </Routes>} />

                    <Route path="/admin/*" element={<Routes>
                      <Route path="dashboard" element={<AdminDashboard />} />
                      <Route path="inventory" element={<AdminInventory />} /> 
                    </Routes>} />
                  </Routes>
                </MainLayout>
             } />
          </Routes>
        </Router>
      </ThemeProvider>
    </AuthProvider>
  );
}