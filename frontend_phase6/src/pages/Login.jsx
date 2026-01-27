import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Auth.css';

const Login = () => {
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [formData, setFormData] = useState({ email: '', password: '', name: '', role: 'patient' });
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (isLoginMode) {
      const result = await login(formData.email, formData.password);
      if (result.success) navigate('/dashboard'); 
      else setError(result.message);
    } else {
      alert('Registration successful! Please log in.');
      setIsLoginMode(true);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2 className="auth-title">{isLoginMode ? 'Welcome Back' : 'Create Account'}</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          {!isLoginMode && (
            <div className="form-group">
              <label>Full Name</label>
              <input type="text" name="name" className="form-input" value={formData.name} onChange={handleChange} required />
            </div>
          )}
          <div className="form-group">
            <label>Email Address</label>
            <input type="email" name="email" className="form-input" value={formData.email} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input type="password" name="password" className="form-input" value={formData.password} onChange={handleChange} required />
          </div>
          {!isLoginMode && (
            <div className="form-group">
              <label>I am a...</label>
              <select name="role" className="form-input" value={formData.role} onChange={handleChange}>
                <option value="patient">Patient</option>
                <option value="doctor">Doctor</option>
                <option value="admin">Administrator</option>
              </select>
            </div>
          )}
          <button type="submit" className="btn-primary">{isLoginMode ? 'Login' : 'Register'}</button>
        </form>
        <p className="toggle-text">
          {isLoginMode ? "Don't have an account?" : "Already have an account?"}
          <span className="toggle-link" onClick={() => setIsLoginMode(!isLoginMode)}>{isLoginMode ? 'Register here' : 'Login here'}</span>
        </p>
      </div>
    </div>
  );
};

export default Login;