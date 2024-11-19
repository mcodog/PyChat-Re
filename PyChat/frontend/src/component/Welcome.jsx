import React, { useContext } from 'react'
import { AuthContext } from '../utils/AuthContext';

const Welcome = () => {
  const { isAuthenticated, userId, loading } = useContext(AuthContext);
  console.log(userId)
  console.log(isAuthenticated)

  return (
    <div>Welcome</div>
  )
}

export default Welcome