import React, { useState } from 'react';
import {
  TextField,
  Button,
  Box,
  Typography,
  Container,
} from '@mui/material';
import axiosInstance from '../utils/AxiosInstace';
import { useNavigate } from 'react-router-dom';

const LoginForm = () => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Login Data:', formData);
  
    try {
      const response = await axiosInstance.post('/login/', formData, { withCredentials: true });
      console.log('Login successful:', response.data);
      // Assuming the backend responds with a message upon success
      localStorage.setItem('token', response.data.token);
      navigate('/'); // Redirect user to homepage or another page upon successful login
    } catch (err) {
      console.error('Login failed:', err.response ? err.response.data : err.message);
      setError('Invalid credentials, please try again.');
    }
  };

  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          mt: 8,
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          Login
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            fullWidth
            label="Username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
            sx={{
                '& .MuiInputBase-root': {
                  padding: '10px', // Adjust padding here
                },
              }}
          />
          <TextField
            margin="normal"
            fullWidth
            label="Password"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            sx={{
                '& .MuiInputBase-root': {
                  padding: '10px', // Adjust padding here
                },
              }}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            sx={{ mt: 3, mb: 2 }}
          >
            Login
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default LoginForm;
