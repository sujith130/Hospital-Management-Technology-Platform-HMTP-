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