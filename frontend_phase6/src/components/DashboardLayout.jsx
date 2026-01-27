import React from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { navItems } from '../config/navConfig';
import '../styles/Dashboard.css';

const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  if (!user) return null;
  const menu = navItems[user.role] || [];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="sidebar-header">MediCare App</div>
        <ul className="nav-links">
          {menu.map((item) => (
            <li key={item.path}>
              <NavLink 
                to={item.path} 
                className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}
              >
                <span className="nav-icon">{item.icon}</span>
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </aside>
      <main className="main-content">
        <header className="top-header">
          <h3>{user.role.charAt(0).toUpperCase() + user.role.slice(1)} Dashboard</h3>
          <div className="user-info">
            <span>Hello, <strong>{user.name || user.email}</strong></span>
            <button onClick={handleLogout} className="logout-btn">Logout</button>
          </div>
        </header>
        <div className="page-content">
          <Outlet /> 
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;