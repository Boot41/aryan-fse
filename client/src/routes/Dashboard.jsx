// /home/aryan/Documents/project/client/src/routes/Dashboard.jsx

import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-4">
      <div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl w-full max-w-2xl border border-gray-700/30">
        <h2 className="text-4xl font-bold text-center text-white mb-8">Development Dashboard</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link
            to="/login"
            className="bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-4 px-6 rounded-lg shadow-md hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200 text-center"
          >
            Login Page
          </Link>
          <Link
            to="/take-assessment"
            className="bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-4 px-6 rounded-lg shadow-md hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200 text-center"
          >
            Take Assessment
          </Link>
          <Link
            to="/create-assessment"
            className="bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-4 px-6 rounded-lg shadow-md hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200 text-center"
          >
            Create Assessment
          </Link>
          <Link
            to="/talk-with-chatbot"
            className="bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-4 px-6 rounded-lg shadow-md hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200 text-center"
          >
            Talk with Chatbot
          </Link>
          <Link
            to="/scheduled-assessments"
            className="bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-4 px-6 rounded-lg shadow-md hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200 text-center"
          >
            Scheduled Assessments
          </Link>
          <Link
            to="/my-profile"
            className="bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-4 px-6 rounded-lg shadow-md hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200 text-center"
          >
            My Profile
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;