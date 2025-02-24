// /home/aryan/Documents/project/client/src/context/UserProvider.jsx

import React, { useState, useEffect } from 'react';
import { UserContext } from './UserContext';
import { authService } from '../services/auth.service';

const UserProvider = ({ children }) => {
  const [state, setState] = useState({
    isAuthenticated: false,
    user: null
  });

  useEffect(() => {
    // Check if user is already logged in
    const currentUser = authService.getCurrentUser();
    if (currentUser) {
      setState({
        isAuthenticated: true,
        user: currentUser
      });
    }
  }, []);

  const login = async (email, password) => {
    try {
      const userData = await authService.login(email, password);
      setState({
        isAuthenticated: true,
        user: userData
      });
      return userData;
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    await authService.logout();
    setState({
      isAuthenticated: false,
      user: null
    });
  };

  return (
    <UserContext.Provider value={{ ...state, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};

export default UserProvider;