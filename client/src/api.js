// /home/aryan/Documents/project/client/src/api.js

const API_BASE_URL = 'http://localhost:8000/api';

// API endpoints
export const registerUser = async (userData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Registration failed');
    }
    
    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const loginUser = async (credentials) => {
  try {
    const response = await fetch(`${API_BASE_URL}/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Login failed');
    }
    
    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const getUserAssignments = async () => {
  try {
    const userEmail = localStorage.getItem('userEmail');
    if (!userEmail) {
      throw new Error('User not logged in');
    }

    const response = await fetch(`${API_BASE_URL}/assignments/?email=${userEmail}`);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch assignments');
    }
    
    return await response.json();
  } catch (error) {
    throw error;
  }
};
