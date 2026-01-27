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