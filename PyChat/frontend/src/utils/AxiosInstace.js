import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'https://pychat-admin.onrender.com/api/', // Replace with your backend API base URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;