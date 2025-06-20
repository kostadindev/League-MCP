# Docker Deployment Guide 🐳

This guide explains how to build and deploy the League MCP Server using Docker.

## Quick Start 🚀

### Using Pre-built Image from Docker Hub
```bash
# Pull and run the image
docker run -e RIOT_API_KEY=your_api_key_here username/league-mcp:latest

# Run with SSE transport (for web integrations)
docker run -p 8000:8000 -e RIOT_API_KEY=your_api_key_here username/league-mcp:latest league-mcp --transport sse
```

### Using Docker Compose
```bash
# Set your API key in environment
export RIOT_API_KEY=your_riot_api_key_here

# Run with docker-compose
docker-compose up
```

## Building Your Own Image 🔨

### Prerequisites
- Docker installed on your system
- Docker Hub account (for publishing)

### Build Locally
```bash
# Build the image
docker build -t league-mcp:latest .

# Test the image
docker run -e RIOT_API_KEY=your_api_key_here league-mcp:latest
```

### Build and Push to Docker Hub

1. **Edit the build script**: Update `DOCKER_USERNAME` in `build-and-push.sh`
2. **Run the build script**:
   ```bash
   # For latest tag
   ./build-and-push.sh

   # For specific version
   ./build-and-push.sh v0.1.2
   ```

## Docker Hub Publishing Steps 📦

### 1. Create Docker Hub Repository
1. Go to [Docker Hub](https://hub.docker.com)
2. Click "Create Repository"
3. Name it `league-mcp`
4. Choose Public or Private
5. Click "Create"

### 2. Build and Tag Your Image
```bash
# Replace 'yourusername' with your Docker Hub username
docker build -t yourusername/league-mcp:latest .

# Tag with version number
docker tag yourusername/league-mcp:latest yourusername/league-mcp:v0.1.2
```

### 3. Push to Docker Hub
```bash
# Login to Docker Hub
docker login

# Push the images
docker push yourusername/league-mcp:latest
docker push yourusername/league-mcp:v0.1.2
```

## Configuration ⚙️

### Environment Variables
- `RIOT_API_KEY`: Your Riot Games API key (required)

### Volumes
The container runs as a non-root user for security. No persistent volumes are required for basic operation.

### Networking
- **Port 8000**: Exposed for SSE transport mode
- **stdio transport**: No ports needed (uses stdin/stdout)

## Usage Examples 💡

### With Claude Desktop Integration
```bash
# Run in stdio mode (default)
docker run -i -e RIOT_API_KEY=your_api_key_here yourusername/league-mcp:latest
```

### With Web Applications
```bash
# Run in SSE mode
docker run -p 8000:8000 -e RIOT_API_KEY=your_api_key_here yourusername/league-mcp:latest league-mcp --transport sse
```

### Development/Testing
```bash
# Use docker-compose for easy development
docker-compose up --build
```

## Multi-Architecture Support 🏗️

To build for multiple architectures (ARM64, AMD64):

```bash
# Create a builder
docker buildx create --name multiarch --use

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t yourusername/league-mcp:latest --push .
```

## Troubleshooting 🔧

### Common Issues

1. **API Key Not Set**
   ```
   Error: RIOT_API_KEY environment variable is required
   ```
   Solution: Ensure you're passing the API key with `-e RIOT_API_KEY=your_key`

2. **Permission Issues**
   The container runs as a non-root user for security. If you need to modify files, use:
   ```bash
   docker run --user root -e RIOT_API_KEY=your_key yourusername/league-mcp:latest
   ```

3. **Port Already in Use**
   ```
   Error: Port 8000 is already in use
   ```
   Solution: Use a different port mapping: `-p 8001:8000`

### Logs and Debugging
```bash
# View container logs
docker logs <container_id>

# Run with verbose logging
docker run -e RIOT_API_KEY=your_key -e LOG_LEVEL=DEBUG yourusername/league-mcp:latest
```

## Security Best Practices 🔒

1. **Never hardcode API keys** in the Dockerfile
2. **Use secrets management** in production
3. **Run as non-root user** (already configured)
4. **Use specific version tags** instead of `latest` in production
5. **Regularly update base images** for security patches

## Performance Optimization 🚀

### Image Size Optimization
The Dockerfile uses:
- `python:3.12-slim` base image (smaller than full Python image)
- Multi-stage builds not needed since we install from PyPI
- `.dockerignore` to exclude unnecessary files

### Runtime Optimization
- Container runs with `PYTHONUNBUFFERED=1` for better logging
- `PYTHONDONTWRITEBYTECODE=1` to avoid .pyc files

## CI/CD Integration 🔄

### GitHub Actions Example
```yaml
name: Build and Push Docker Image

on:
  push:
    tags: [ 'v*' ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: ./mcp-server
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/league-mcp:latest
          ${{ secrets.DOCKER_USERNAME }}/league-mcp:${{ github.ref_name }}
```

## Support 💬

For Docker-related issues:
1. Check this documentation
2. Review container logs
3. Open an issue on GitHub with Docker version and error details 