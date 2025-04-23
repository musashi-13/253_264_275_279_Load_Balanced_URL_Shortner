#!/bin/bash

# Create static directory if it doesn't exist
mkdir -p src/url-shortener/static

echo "Setting up URL Shortener..."

echo "Building and starting Docker containers..."
docker-compose up -d

echo "URL Shortener is now running!"
echo "You can access it at: http://localhost:5000"
echo "API documentation available at: http://localhost:5000/api"

echo "To stop the containers, run: docker-compose down" 