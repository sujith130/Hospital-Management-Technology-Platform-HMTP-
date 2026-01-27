import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  // Default to 'doctor' to show off the complex UI first
  const [userRole, setUserRole] = useState('doctor'); 

  const login = (role) => setUserRole(role);
  const logout = () => setUserRole(null);

  return (
    <AuthContext.Provider value={{ userRole, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);