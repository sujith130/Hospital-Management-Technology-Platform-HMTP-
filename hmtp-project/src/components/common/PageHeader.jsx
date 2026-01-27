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