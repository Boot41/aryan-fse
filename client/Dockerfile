# Use the official Node.js image
FROM node:latest

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port for Vite
EXPOSE 5173

# Command to run the Vite app
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
