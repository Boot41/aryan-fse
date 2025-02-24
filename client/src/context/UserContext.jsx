// /home/aryan/Documents/project/client/src/context/UserContext.jsx

import { createContext, useContext } from 'react';

// Create the context with default values
const UserContext = createContext({
  isAuthenticated: false,
  user: null,
  login: () => {},
  logout: () => {},
});

// Export the context
export { UserContext };

// Export a custom hook for easier usage
export const useUser = () => useContext(UserContext);