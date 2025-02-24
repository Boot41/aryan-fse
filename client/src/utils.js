// Get user data from localStorage
export const getUserData = () => {
  const userData = localStorage.getItem('userData');
  return userData ? JSON.parse(userData) : null;
};

// Get auth token from localStorage
export const getToken = () => {
  return localStorage.getItem('token');
};

// Clear user data (for logout)
export const clearUserData = () => {
  localStorage.removeItem('userData');
  localStorage.removeItem('token');
};
