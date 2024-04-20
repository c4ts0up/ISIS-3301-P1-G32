# Use Node.js as the base image
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the entire project to the working directory
COPY . .

# Build the React app for production
RUN npm run build

# Install serve globally
RUN npm install -g serve

# Expose port 3000 to the outside world
EXPOSE 3000

# Command to run the React app
CMD ["serve", "-s", "build"]
