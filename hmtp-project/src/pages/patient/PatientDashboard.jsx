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