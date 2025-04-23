# Load Balanced URL Shortener

A scalable URL shortener built with Python, Docker, and Kubernetes. It shortens URLs via an API, uses Redis for storage, and features load balancing, autoscaling, and Ingress routing.

## Project Overview

This URL shortener is designed to be scalable and resilient, with the following components:

- **Frontend**: Simple HTML interface for URL shortening
- **Backend**: Flask API for URL shortening functionality
- **Database**: Redis for fast and efficient storage of URL mappings
- **Containerization**: Docker for packaging the application
- **Orchestration**: Kubernetes for container management, scaling, and load balancing

## Setup Options

### Option 1: Local Development with Docker Compose (Recommended for Development)

This is the easiest way to run the application locally:

1. **Prerequisites**:
   - Docker and Docker Compose installed on your machine
   - Git (to clone this repository)

2. **Setup**:
   ```bash
   # Clone the repository
   git clone https://github.com/musashi-13/253_264_275_279_Load_Balanced_URL_Shortner.git
   cd 253_264_275_279_Load_Balanced_URL_Shortner
   
   # Run the setup script
   ./setup.sh
   ```

3. **Access the application**:
   - Web interface: http://localhost:5000
   - API documentation: http://localhost:5000/api

4. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Option 2: Kubernetes Deployment (Recommended for Production)

For a more robust, scalable deployment:

1. **Prerequisites**:
   - Kubernetes cluster (local like Minikube or a cloud provider)
   - kubectl configured to work with your cluster
   - Docker (for building the image)

2. **Build and push the Docker image**:
   ```bash
   cd src/url-shortener
   docker build -t your-docker-username/url-shortener:latest .
   docker push your-docker-username/url-shortener:latest
   ```

3. **Update the deployment file**:
   Edit `kubes/url-shortener-deployment.yaml` and change the image name:
   ```yaml
   image: your-docker-username/url-shortener:latest
   ```

4. **Apply the Kubernetes configurations**:
   ```bash
   kubectl apply -f kubes/configmap.yaml
   kubectl apply -f kubes/redis-deployment.yaml
   kubectl apply -f kubes/url-shortener-deployment.yaml
   ```

5. **Access the application**:
   ```bash
   kubectl get service url-shortener
   ```
   Use the external IP or port forwarding to access the service.

## API Usage

### Shorten a URL

```bash
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/url"}'
```

Response:
```json
{
  "short_url": "http://localhost:5000/abc123"
}
```

### Redirect to Original URL

Simply visit the short URL in your browser, or use:

```bash
curl -L http://localhost:5000/abc123
```

## Project Structure

```
.
├── docker-compose.yml         # Docker Compose configuration for local development
├── kubes/                     # Kubernetes configuration files
│   ├── configmap.yaml         # ConfigMap for environment variables
│   ├── redis-deployment.yaml  # Redis deployment and service
│   └── url-shortener-deployment.yaml  # URL shortener deployment and service
└── src/
    └── url-shortener/         # URL shortener application
        ├── Dockerfile         # Docker configuration
        ├── app.py             # Flask application
        ├── requirements.txt   # Python dependencies
        └── static/            # Static files for web interface
            └── index.html     # Simple HTML frontend
```

## Local Development

To modify the application:

1. Make changes to the code
2. Rebuild and restart the containers:
   ```bash
   docker-compose down
   docker-compose up --build -d
   ```

## Future Enhancements

- Add persistent storage for Redis
- Implement user authentication
- Add analytics for URL clicks
- Create custom short codes
- Implement URL expiration
