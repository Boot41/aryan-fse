// /home/aryan/Documents/project/client/src/components/LoginPage.jsx

import React from 'react';
import LoginForm from './LoginForm';
import { Link } from 'react-router-dom';

const LoginPage = () => {
  const handleLogin = (credentials) => {
    console.log('Login Credentials:', credentials);
    // Handle login logic here
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-4">
      <div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl w-full max-w-md border border-gray-700/30">
        <h2 className="text-4xl font-bold text-center text-white mb-8">Welcome Back</h2>
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