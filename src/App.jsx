import React from 'react'
import {BrowserRouter as Router,Routes,Route}from 'react-router-dom';
import Dashboard from './components/Dashboard'
import Login from './components/Login';
const App = () => {
  return (
    <div>
      <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      </Router>
    </div>
  )
}

export default App
