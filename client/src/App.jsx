// /home/aryan/Documents/project/client/src/App.jsx

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import TakeAssessment from './routes/TakeAssessment';
import TalkWithChatbot from './routes/TalkWithChatbot';
import ScheduledAssessments from './routes/ScheduledAssessments';
import MyProfile from './routes/MyProfile';
import Dashboard from './routes/Dashboard';
import SignupPage from './routes/SignupPage';
import LoginPage from './routes/LoginPage';
import Assignments from './routes/Assignments';
import Navbar from './components/common/Navbar';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Add logic to check authentication status (e.g., from localStorage or API)
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
  }, []);

  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={isAuthenticated ? <Navigate to="/my-profile"/> : <Navigate to="/login"/>}/>
        <Route path="/login" element={<LoginPage/>}/>
        <Route path="/signup" element={<SignupPage/>}/>
        <Route path="/take-assessment" element={<TakeAssessment/>}/>
        <Route path="/chatbot" element={<TalkWithChatbot/>}/>
        <Route path="/scheduled-assessments" element={<ScheduledAssessments/>}/>
        <Route path="/my-profile" element={<MyProfile/>}/>
        <Route path="/dashboard" element={<Dashboard />}/>
        <Route path='/assignments' element={<Assignments />}/>
      </Routes>
    </Router>
  );
}

export default App;