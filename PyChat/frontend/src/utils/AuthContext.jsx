import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import axiosInstance from '../utils/AxiosInstace';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState()
  const [userId, setUserId] = useState()

  useEffect(() => {
    const fetchAuthStatus = async () => {
      try {
        console.log(isAuthenticated)
        const response = await axiosInstance.get('/auth/status/');

        try {
          const token = localStorage.getItem('token');
          if (!token) {
              throw new Error('No token found');
          }
          const strippedToken = token.replace('Bearer ', '');
          console.log('Authenticated with token:', strippedToken);

          const base64Url = token.split('.')[1]; // The payload is the second part of the token
          const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/'); // Convert to Base64 format
          const payload = JSON.parse(atob(base64)); // Decode and parse to JSON
          
          setIsAuthenticated(true);
          setUser(payload.username);
          setUserId(payload.id)
      } catch (error) {
          console.error('Failed to check authentication status:', error.message);
      }
      
      } catch (error) {
        console.error('Failed to check authentication status:', error);
        setIsAuthenticated(false);
        setUser(null);
        setUserId(null);
      } finally {
        setLoading(false);
      }
    };

    fetchAuthStatus();
  }, []);

  return (
    <AuthContext.Provider value={{ user, userId, isAuthenticated, loading }}>
      {loading ? <div></div> : children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);