// /home/aryan/Documents/project/client/src/App.jsx

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import HomePage from './routes/HomePage';
import TakeAssessment from './routes/TakeAssessment';
import CreateAssessment from './routes/CreateAssessment';
import TalkWithChatbot from './routes/TalkWithChatbot';
import ScheduledAssessments from './routes/ScheduledAssessments';
import MyProfile from './routes/MyProfile';
import Dashboard from './routes/Dashboard';
import SignupPage from './routes/SignupPage';
import Assessments from './routes/Assessments';
import Navbar from './components/common/Navbar';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/take-assessment" element={<TakeAssessment />} />
        <Route path="/create-assessment" element={<CreateAssessment />} />
        <Route path="/chatbot" element={<TalkWithChatbot />} />
        <Route path="/scheduled-assessments" element={<ScheduledAssessments />} />
        <Route path="/my-profile" element={<MyProfile />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path='/assessments' element={<Assessments />} />
      </Routes>
    </Router>
  );
}

export default App;