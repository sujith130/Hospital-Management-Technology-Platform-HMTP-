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