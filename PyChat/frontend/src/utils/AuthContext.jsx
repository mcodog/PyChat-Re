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
        const response = await axiosInstance.get('/auth/status/');
        setIsAuthenticated(response.data.isAuthenticated);
        setUser(response.data.isAuthenticated ? response.data.username : null);
        console.log(response.data)
        setUserId(response.data.isAuthenticated ? response.data.id : null)
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