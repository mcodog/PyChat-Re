import './App.css'
import { Routes, Route } from 'react-router-dom'
import Layout from './component/Layout'
import Welcome from './component/Welcome'
import Chat from './component/Chat'
import ChatList from './component/ChatList'

function App() {

  return (
    <>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Welcome />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/chatlist" element={<ChatList />} />
        </Route>
      </Routes>
    </>
  )
}

export default App
