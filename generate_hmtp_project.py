import os

# Define the project structure and file contents
project_name = "hmtp-project"

files = {
    "package.json": """
{
  "name": "hmtp-client",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.14.16",
    "@mui/material": "^5.14.16",
    "@mui/x-data-grid": "^6.18.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.18.0",
    "recharts": "^2.9.3"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@vitejs/plugin-react": "^4.2.0",
    "eslint": "^8.53.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "vite": "^5.0.0"
  }
}
""",
    "vite.config.js": """
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})
""",
    "index.html": """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap"
    />
    <title>HMTP Professional Platform</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""",
    "src/main.jsx": """
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""",
    "src/App.jsx": """
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
""",
    "src/context/AuthContext.jsx": """
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  // Default to 'doctor' to show off the complex UI first
  const [userRole, setUserRole] = useState('doctor'); 

  const login = (role) => setUserRole(role);
  const logout = () => setUserRole(null);

  return (
    <AuthContext.Provider value={{ userRole, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
""",
    "src/components/layout/MainLayout.jsx": """
import React, { useState } from 'react';
import { Box, AppBar, Toolbar, IconButton, Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Avatar, Typography, Divider, Button } from '@mui/material';
import { Menu, Dashboard, CalendarMonth, People, Medication, Settings, LocalHospital, Inventory, Logout } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const drawerWidth = 260;

export default function MainLayout({ children }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { userRole, logout, login } = useAuth(); // Get current role
  const navigate = useNavigate();

  // Define menus for each role
  const menus = {
    patient: [
      { text: 'My Health', icon: <Dashboard />, path: '/patient/dashboard' },
      { text: 'Appointments', icon: <CalendarMonth />, path: '/patient/appointments' },
      { text: 'Prescriptions', icon: <Medication />, path: '/patient/prescriptions' },
    ],
    doctor: [
      { text: 'Doctor Console', icon: <Dashboard />, path: '/doctor/dashboard' },
      { text: 'My Schedule', icon: <CalendarMonth />, path: '/doctor/schedule' },
      { text: 'Patients', icon: <People />, path: '/doctor/patients' },
    ],
    admin: [
      { text: 'Admin Overview', icon: <Dashboard />, path: '/admin/dashboard' },
      { text: 'Inventory', icon: <Inventory />, path: '/admin/inventory' },
      { text: 'Staff Mgmt', icon: <People />, path: '/admin/staff' },
    ]
  };

  const currentMenu = menus[userRole] || [];

  const drawerContent = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Toolbar sx={{ bgcolor: 'primary.main', color: 'white', gap: 1 }}>
        <LocalHospital />
        <Typography variant="h6" fontWeight="bold">HMTP Core</Typography>
      </Toolbar>
      
      {/* Role Switcher for Demo Purposes */}
      <Box sx={{ p: 2, bgcolor: '#f5f5f5' }}>
        <Typography variant="caption" display="block" sx={{ mb: 1 }}>VIEW AS (DEMO):</Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button size="small" variant={userRole === 'patient' ? "contained" : "outlined"} onClick={() => login('patient')}>Pt</Button>
          <Button size="small" variant={userRole === 'doctor' ? "contained" : "outlined"} onClick={() => login('doctor')}>Dr</Button>
          <Button size="small" variant={userRole === 'admin' ? "contained" : "outlined"} onClick={() => login('admin')}>Ad</Button>
        </Box>
      </Box>

      <List sx={{ flexGrow: 1, pt: 2 }}>
        {currentMenu.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton onClick={() => navigate(item.path)}>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider />
      <List>
        <ListItem disablePadding>
          <ListItemButton onClick={logout}>
            <ListItemIcon><Logout /></ListItemIcon>
            <ListItemText primary="Log Out" />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed" sx={{ width: { sm: `calc(100% - ${drawerWidth}px)` }, ml: { sm: `${drawerWidth}px` } }}>
        <Toolbar>
          <IconButton color="inherit" edge="start" onClick={() => setMobileOpen(!mobileOpen)} sx={{ mr: 2, display: { sm: 'none' } }}>
            <Menu />
          </IconButton>
          <Box sx={{ flexGrow: 1 }} />
          <Avatar sx={{ bgcolor: 'secondary.main' }}>{userRole?.[0]?.toUpperCase()}</Avatar>
        </Toolbar>
      </AppBar>

      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
        <Drawer variant="temporary" open={mobileOpen} onClose={() => setMobileOpen(!mobileOpen)} sx={{ display: { xs: 'block', sm: 'none' }, '& .MuiDrawer-paper': { width: drawerWidth } }}>
          {drawerContent}
        </Drawer>
        <Drawer variant="permanent" sx={{ display: { xs: 'none', sm: 'block' }, '& .MuiDrawer-paper': { width: drawerWidth } }} open>
          {drawerContent}
        </Drawer>
      </Box>

      <Box component="main" sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` }, bgcolor: '#f4f6f8', minHeight: '100vh' }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
}
""",
    "src/components/common/PageHeader.jsx": """
import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';

export default function PageHeader({ title, subtitle, actionLabel, onAction }) {
  return (
    <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <Box>
        <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#1a2027' }}>{title}</Typography>
        {subtitle && <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>{subtitle}</Typography>}
      </Box>
      {actionLabel && (
        <Button variant="contained" startIcon={<AddIcon />} onClick={onAction} size="large">
          {actionLabel}
        </Button>
      )}
    </Box>
  );
}
""",
    "src/pages/public/LandingPage.jsx": """
import React from 'react';
import { Box, Container, Typography, Button, Grid, Paper, TextField, InputAdornment } from '@mui/material';
import { Search, MedicalServices, EventAvailable, LocalHospital } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <Box>
      {/* Hero Section */}
      <Box sx={{ bgcolor: 'primary.main', color: 'white', py: 10, position: 'relative', overflow: 'hidden' }}>
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h2" sx={{ fontWeight: '800', mb: 2 }}>
                Advanced Care, <br /> Compassionate Hearts.
              </Typography>
              <Typography variant="h6" sx={{ mb: 4, opacity: 0.9 }}>
                The region's leading HMTP platform connecting you with top specialists instantly.
              </Typography>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button variant="contained" color="secondary" size="large" onClick={() => navigate('/auth/login')}>
                  Patient Portal
                </Button>
                <Button variant="outlined" color="inherit" size="large" onClick={() => navigate('/doctors')}>
                  Find a Doctor
                </Button>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Services Grid */}
      <Container sx={{ py: 8 }}>
        <Typography variant="h4" textAlign="center" sx={{ mb: 6, fontWeight: 'bold' }}>Our Services</Typography>
        <Grid container spacing={4}>
          {[
            { title: 'Emergency Care', icon: <LocalHospital />, desc: '24/7 Trauma center access.' },
            { title: 'Online Booking', icon: <EventAvailable />, desc: 'Book appointments in 30 seconds.' },
            { title: 'Specialized Depts', icon: <MedicalServices />, desc: 'Cardiology, Neurology & more.' }
          ].map((item, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Paper sx={{ p: 4, textAlign: 'center', height: '100%' }}>
                <Box sx={{ color: 'primary.main', mb: 2, '& svg': { fontSize: 50 } }}>{item.icon}</Box>
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>{item.title}</Typography>
                <Typography color="text.secondary">{item.desc}</Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
}
""",
    "src/pages/patient/PatientDashboard.jsx": """
import React from 'react';
import { Grid, Paper, Typography, Box, Button, Chip } from '@mui/material';
import { MonitorHeart, Event, MedicalServices } from '@mui/icons-material';
import PageHeader from '../../components/common/PageHeader';

const Stat = ({ title, value, icon, color }) => (
  <Paper sx={{ p: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
    <Box>
      <Typography color="text.secondary">{title}</Typography>
      <Typography variant="h4" fontWeight="bold">{value}</Typography>
    </Box>
    <Box sx={{ color, bgcolor: `${color}20`, p: 1, borderRadius: 1 }}>{icon}</Box>
  </Paper>
);

export default function PatientDashboard() {
  return (
    <Box>
      <PageHeader title="Welcome back, Sarah" subtitle="Health ID: P-902-11" actionLabel="New Appointment" />
      
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}><Stat title="Blood Pressure" value="120/80" icon={<MonitorHeart />} color="#d32f2f" /></Grid>
        <Grid item xs={12} md={4}><Stat title="Next Visit" value="Oct 24" icon={<Event />} color="#1976d2" /></Grid>
        <Grid item xs={12} md={4}><Stat title="Active Meds" value="3" icon={<MedicalServices />} color="#2e7d32" /></Grid>
      </Grid>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>Upcoming Appointments</Typography>
        {[1, 2].map((i) => (
          <Box key={i} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', p: 2, mb: 1, border: '1px solid #eee', borderRadius: 2 }}>
            <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
              <Box sx={{ textAlign: 'center', p: 1, bgcolor: '#e3f2fd', borderRadius: 1, minWidth: 60 }}>
                <Typography variant="h6" color="primary" fontWeight="bold">2{i}</Typography>
                <Typography variant="caption">OCT</Typography>
              </Box>
              <Box>
                <Typography fontWeight="bold">Dr. Sarah Smith</Typography>
                <Typography variant="body2" color="text.secondary">Cardiology • General Checkup</Typography>
              </Box>
            </Box>
            <Chip label="Confirmed" color="success" size="small" />
          </Box>
        ))}
      </Paper>
    </Box>
  );
}
""",
    "src/pages/doctor/DoctorDashboard.jsx": """
import React from 'react';
import { Grid, Paper, Typography, Box, Avatar, Divider, List, ListItem, ListItemText, ListItemAvatar } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import PageHeader from '../../components/common/PageHeader';

const patientRows = [
  { id: 1, name: 'James Howlett', age: 45, reason: 'Chronic Pain', time: '09:00 AM', status: 'In Progress' },
  { id: 2, name: 'Wade Wilson', age: 32, reason: 'Skin Burn', time: '09:30 AM', status: 'Waiting' },
  { id: 3, name: 'Jean Grey', age: 28, reason: 'Headaches', time: '10:00 AM', status: 'Scheduled' },
];

const columns = [
  { field: 'time', headerName: 'Time', width: 100 },
  { field: 'name', headerName: 'Patient', width: 180 },
  { field: 'reason', headerName: 'Complaint', width: 200 },
  { field: 'status', headerName: 'Status', width: 120 },
];

export default function DoctorDashboard() {
  return (
    <Box>
      <PageHeader title="Doctor's Console" subtitle="Dr. Strange - Neurology Dept" />

      <Grid container spacing={3}>
        {/* Main Schedule */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ height: 500, p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>Today's Schedule</Typography>
            <DataGrid rows={patientRows} columns={columns} checkboxSelection disableSelectionOnClick />
          </Paper>
        </Grid>

        {/* Notifications & Urgent */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, color: 'error.main' }}>Critical Alerts</Typography>
            <List dense>
              <ListItem>
                <ListItemAvatar><Avatar sx={{ bgcolor: 'error.light' }}>!</Avatar></ListItemAvatar>
                <ListItemText primary="ICU Bed Capacity Low" secondary="Only 2 beds remaining in Ward A" />
              </ListItem>
            </List>
          </Paper>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>Pending Lab Results</Typography>
            <List>
               <ListItem>
                 <ListItemText primary="P-902 (Blood Work)" secondary="Ready for review" />
               </ListItem>
               <Divider />
               <ListItem>
                 <ListItemText primary="P-881 (X-Ray)" secondary="Processing..." />
               </ListItem>
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
""",
    "src/pages/admin/AdminDashboard.jsx": """
import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import PageHeader from '../../components/common/PageHeader';

const data = [
  { name: 'Mon', patients: 40 },
  { name: 'Tue', patients: 30 },
  { name: 'Wed', patients: 55 },
  { name: 'Thu', patients: 45 },
  { name: 'Fri', patients: 70 },
];

export default function AdminDashboard() {
  return (
    <Box>
      <PageHeader title="Hospital Administration" subtitle="Main Overview" />
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h4" color="primary" fontWeight="bold">85%</Typography>
            <Typography color="text.secondary">Bed Occupancy</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h4" color="success.main" fontWeight="bold">$42k</Typography>
            <Typography color="text.secondary">Daily Revenue</Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={12}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>Weekly Patient Inflow</Typography>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="patients" fill="#1976d2" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
""",
    "src/pages/admin/AdminInventory.jsx": """
import React from 'react';
import { Box, Chip } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import PageHeader from '../../components/common/PageHeader';

const columns = [
  { field: 'id', headerName: 'Item ID', width: 90 },
  { field: 'name', headerName: 'Item Name', width: 200 },
  { field: 'category', headerName: 'Category', width: 150 },
  { field: 'stock', headerName: 'Stock Level', width: 130, renderCell: (params) => (
      <Chip label={params.value} color={params.value < 20 ? 'error' : 'success'} variant="filled" size="small" />
    ) 
  },
  { field: 'price', headerName: 'Unit Price', width: 120 },
];

const rows = [
  { id: 'M-101', name: 'Paracetamol 500mg', category: 'Medicine', stock: 500, price: '$0.50' },
  { id: 'S-202', name: 'Surgical Masks', category: 'Supplies', stock: 15, price: '$1.20' }, // Low stock
  { id: 'E-303', name: 'Syringes 5ml', category: 'Equipment', stock: 1200, price: '$0.20' },
];

export default function AdminInventory() {
  return (
    <Box>
      <PageHeader title="Inventory Management" actionLabel="Add New Item" />
      <Box sx={{ height: 600, width: '100%', bgcolor: 'white' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          pageSize={10}
          checkboxSelection
          disableSelectionOnClick
        />
      </Box>
    </Box>
  );
}
"""
}

# Create directories and files
if not os.path.exists(project_name):
    os.makedirs(project_name)

for filepath, content in files.items():
    full_path = os.path.join(project_name, filepath)
    directory = os.path.dirname(full_path)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip())

print(f"Created '{project_name}' with {len(files)} files.")

