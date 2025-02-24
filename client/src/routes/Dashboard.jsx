// /home/aryan/Documents/project/client/src/routes/Dashboard.jsx

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getUserProfile } from '../services/api';

function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getUserProfile();
        setProfile(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-4">
      {/* Profile Stats Section */}
      {loading ? (
        <div className="text-center p-4 text-white">Loading profile...</div>
      ) : error ? (
        <div className="text-red-500 p-4">{error}</div>
      ) : profile ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-gray-800/70 backdrop-blur-sm rounded-lg p-6 text-white border border-gray-700/30">
            <h3 className="text-lg font-semibold mb-2">Total Assignments</h3>
            <p className="text-3xl">{profile.stats.total_assignments}</p>
          </div>
          <div className="bg-gray-800/70 backdrop-blur-sm rounded-lg p-6 text-white border border-gray-700/30">
            <h3 className="text-lg font-semibold mb-2">Completed</h3>
            <p className="text-3xl">{profile.stats.completed_assignments}</p>
          </div>
          <div className="bg-gray-800/70 backdrop-blur-sm rounded-lg p-6 text-white border border-gray-700/30">
            <h3 className="text-lg font-semibold mb-2">Average Score</h3>
            <p className="text-3xl">{profile.stats.average_score.toFixed(1)}%</p>
          </div>
          <div className="bg-gray-800/70 backdrop-blur-sm rounded-lg p-6 text-white border border-gray-700/30">
            <h3 className="text-lg font-semibold mb-2">Pending</h3>
            <p className="text-3xl">{profile.stats.pending_assignments}</p>
          </div>
        </div>
      ) : null}

      {/* Navigation Cards Section */}
      <div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl border border-gray-700/30">
        <h2 className="text-3xl font-bold text-white mb-8">Student Portal</h2>
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
            to="/chatbot"
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
}

export default Dashboard;