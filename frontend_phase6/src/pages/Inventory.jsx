import React, { useState, useEffect } from 'react';
import '../styles/Table.css';
import api from '../services/api';

const Inventory = () => {
  const [medicines, setMedicines] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMedicines = async () => {
      try {
        const res = await api.get('/pharmacy/medicines/');
        setMedicines(res.data);
      } catch (error) {
        console.error("Fetch Error:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchMedicines();
  }, []);

  if (loading) return <div>Loading inventory...</div>;

  return (
    <div>
      <div className="page-header"><h2>Pharmacy Inventory</h2><button className="btn-add">+ Add Medicine</button></div>
      <div className="data-table-container">
        <table className="data-table">
          <thead><tr><th>Name</th><th>Batch</th><th>Expiry</th><th>Stock</th><th>Price</th></tr></thead>
          <tbody>
            {medicines.map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td><td>{item.batch_number || 'N/A'}</td><td>{item.expiry_date}</td>
                <td><span className={`status-badge ${item.quantity < 10 ? 'status-inactive' : 'status-active'}`} style={item.quantity < 10 ? { color: 'red' } : {}}>{item.quantity}</span></td>
                <td>${item.unit_price.toFixed(2)}</td>
              </tr>
            ))}
            {medicines.length === 0 && <tr><td colSpan="5" style={{ textAlign: 'center' }}>No stock available</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
};
export default Inventory;