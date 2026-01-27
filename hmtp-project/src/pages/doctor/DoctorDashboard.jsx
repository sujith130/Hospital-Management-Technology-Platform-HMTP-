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