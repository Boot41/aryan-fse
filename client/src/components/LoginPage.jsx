// /home/aryan/Documents/project/client/src/components/LoginPage.jsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import LoginForm from './LoginForm';
import { useUser } from '../context/UserContext';

const LoginPage = () => {
  const [error, setError] = useState('');
  const { login } = useUser();
  const navigate = useNavigate();

  const handleLogin = async (credentials) => {
    try {
      setError('');
      const userData = await login(credentials.email, credentials.password);
      
      if (userData.user_type === 'teacher') {
        navigate('/dashboard');
      } else if (userData.user_type === 'student') {
        navigate('/assessments');
      } else {
        navigate('/dashboard');
      }
    } catch (error) {
      setError(error.response?.data?.error || 'Login failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-4">
      <div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl w-full max-w-md border border-gray-700/30">
        <h2 className="text-4xl font-bold text-center text-white mb-8">Welcome Back</h2>
        {error && (
          <div className="mb-4 p-3 bg-red-500/10 border border-red-500/20 rounded text-red-500 text-sm">
            {error}
          </div>
        )}
        <LoginForm onSubmit={handleLogin} />
        <p className="text-center text-gray-400 mt-6">
          Don't have an account?{' '}
          <Link to="/signup" className="text-purple-400 hover:text-purple-300 underline">
            Sign Up
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;