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