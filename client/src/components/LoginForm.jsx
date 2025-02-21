// /home/aryan/Documents/project/client/src/components/LoginForm.jsx

import React, { useState } from 'react';

const LoginForm = ({ onSubmit }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ email, password });
  };

  return (
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
          />
        </div>
      </div>
      <div className="flex items-center justify-between">
        <a href="#" className="text-sm font-medium text-purple-400 hover:text-purple-300">
          Forgot Password?
        </a>
      </div>
      <div>
        <button
          type="submit"
          className="w-full bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-2 px-4 rounded-lg shadow-md hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200"
        >
          Sign In
        </button>
      </div>
    </form>
  );
};

export default LoginForm;