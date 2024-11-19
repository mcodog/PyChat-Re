import React, { useContext } from 'react';
import { AuthContext } from '../utils/AuthContext'; // Adjust the path to your AuthContext
import axios from 'axios';
import axiosInstance from '../utils/AxiosInstace';

const Logout = () => {
  // const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value || document.cookie.split('csrftoken=')[1]?.split(';')[0];

  const { setIsAuthenticated, setUser } = useContext(AuthContext);

  const handleLogout = async () => {
    try {
      await axiosInstance.post('/logout/');

      window.location.href = '/login'; // Change to your desired path
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <button onClick={handleLogout}>Logout</button>
  );
};

export default Logout;
