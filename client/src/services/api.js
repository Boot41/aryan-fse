import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // This is important for sending cookies
});

// Function to get CSRF token
const getCSRFToken = async () => {
  try {
    const response = await api.get('api/csrf-token/');
    return response.data.csrfToken;
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
    throw error;
  }
};

// Add a request interceptor for handling tokens
api.interceptors.request.use(
  async (config) => {
    // Don't get CSRF token for the CSRF token endpoint itself
    if (!config.url.endsWith('csrf-token/')) {
      try {
        const token = await getCSRFToken();
        config.headers['X-CSRFToken'] = token;
      } catch (error) {
        console.error('Failed to get CSRF token:', error);
      }
    }

    // Add auth token if it exists
    const authToken = localStorage.getItem('token');
    if (authToken) {
      config.headers.Authorization = `Bearer ${authToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Function to get user profile
export const getUserProfile = async () => {
  try {
    const email = localStorage.getItem('userEmail');  // Get email from localStorage
    const response = await api.get(`api/profile/?email=${email}`);
    return response.data.profile;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

export default api;
