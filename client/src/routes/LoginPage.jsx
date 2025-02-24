import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { loginUser } from '../api';

const LoginPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await loginUser({ email, password });
      // Store only user name and email
      localStorage.setItem('userName', response.user.name);
      localStorage.setItem('userEmail', response.user.email);
      
      // Redirect to dashboard
      navigate('/dashboard');
    } catch (error) {
      setError(error.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-4">
      <div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl w-full max-w-md border border-gray-700/30">
        <h2 className="text-4xl font-bold text-center text-white mb-8">Login</h2>
        {error && (
          <div className="mb-4 p-3 bg-red-500/20 border border-red-500/50 rounded text-red-200 text-sm">
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-300">
              Email
            </label>
            <div className="mt-1">
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-gray-700 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent bg-gray-800 text-white"
                placeholder="Enter your email"
                required
                disabled={loading}
              />
            </div>
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-300">
              Password
            </label>
            <div className="mt-1">
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-gray-700 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent bg-gray-800 text-white"
                placeholder="Enter your password"
                required
                disabled={loading}
              />
            </div>
          </div>
          <div>
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-2 px-4 rounded-lg shadow-md hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50"
              disabled={loading}
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </div>
        </form>
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
