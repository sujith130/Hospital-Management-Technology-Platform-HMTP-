import React, { useState, useEffect } from 'react';
import api from '../services/api';
import '../styles/Billing.css';
import '../styles/Table.css';

const Billing = () => {
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(true);
  const items = [{ id: 1, name: 'Consultation Fee', price: 50.00 }, { id: 2, name: 'General Medicine', price: 15.00 }];
  const [cart, setCart] = useState([]);

  const fetchInvoices = async () => {
    try {
      // For demo, we just fetch for a default patient
      const res = await api.get('/billing/invoices/patient/1');
      setInvoices(res.data);
    } catch (error) {
      console.error("Fetch Invoices Error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInvoices();
  }, []);

  const addToCart = (item) => setCart([...cart, item]);
  const total = cart.reduce((acc, item) => acc + item.price, 0).toFixed(2);

  const handleBillGenerate = async () => {
    try {
      const billData = {
        patient_id: 1,
        total_amount: parseFloat(total),
        final_amount: parseFloat(total) * 1.1, // with simplified tax
        tax_amount: parseFloat(total) * 0.1,
        status: "unpaid"
      };
      await api.post('/billing/invoices/', billData);
      alert("Invoice generated successfully!");
      setCart([]);
      fetchInvoices();
    } catch (error) {
      alert("Billing failed: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  return (
    <div className="billing-container">
      <div className="billing-panel" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div className="billing-card">
          <h3>Add Items</h3>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            {items.map(i => <button key={i.id} className="btn-sm" onClick={() => addToCart(i)}>{i.name} (${i.price})</button>)}
          </div>
          <div style={{ marginTop: '20px' }}>
            <h4>Cart</h4>
            <ul className="invoice-item-list">{cart.map((i, idx) => <li key={idx} className="invoice-item"><span>{i.name}</span><span>${i.price}</span></li>)}</ul>
            {cart.length > 0 && <button className="btn-primary" onClick={handleBillGenerate}>Generate Invoice (${(total * 1.1).toFixed(2)})</button>}
          </div>
        </div>
        <div className="billing-card">
          <h3>Recent Invoices</h3>
          {loading ? <div>Loading...</div> : (
            <table className="data-table">
              <thead><tr><th>ID</th><th>Amount</th><th>Status</th></tr></thead>
              <tbody>
                {invoices.map(inv => (
                  <tr key={inv.id}>
                    <td>#{inv.id}</td><td>${inv.final_amount.toFixed(2)}</td>
                    <td><span className={`status-badge status-${inv.status}`}>{inv.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};
export default Billing;