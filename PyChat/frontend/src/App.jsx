import './App.css'
import { Routes, Route } from 'react-router-dom'
import Layout from './component/Layout'
import Welcome from './component/Welcome'
import Chat from './component/Chat'
import ChatList from './component/ChatList'
import Login from './component/Login'
import Register from './component/Register'
import { AuthProvider } from './utils/AuthContext';
import ProtectedRoute from './utils/ProtectedRoute';
import axios from 'axios'
import Logout from './component/Logout'
import Task from './component/Task'

function App() {
  axios.defaults.withCredentials = true;
  // axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
  axios.defaults.headers['X-CSRFToken'] = document.cookie.match(/csrftoken=([^;]+)/)[1];

  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route element={<ProtectedRoute />}>
            <Route path="/chat" element={<Chat />} />
            <Route path="/chatlist" element={<ChatList />} />
            <Route path="/tasks" element={<Task />} />
            <Route index element={<Welcome />} />
          </Route>

          
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/logout" element={<Logout />} />
        </Route>
      </Routes>
    </AuthProvider>
  )
}

export default App
