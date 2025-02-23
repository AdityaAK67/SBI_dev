# Use the official Node.js image from Docker Hub
FROM node:latest

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (if available) first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Set environment variable to suppress Node.js warnings
ENV NODE_OPTIONS=--no-warnings

# Expose the port Vite uses (usually 5173)
EXPOSE 5173

# Command to run the React application
CMD ["npm", "run", "dev"]
