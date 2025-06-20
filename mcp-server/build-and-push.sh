#!/bin/bash

# Build and push script for League MCP Server Docker image
# Usage: ./build-and-push.sh [tag]

set -e

# Configuration
DOCKER_USERNAME="kostadindev"  # Change this to your Docker Hub username
IMAGE_NAME="league-mcp"
TAG=${1:-latest}
FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"

echo "Building Docker image: ${FULL_IMAGE_NAME}"

# Build the image
docker build -t "${FULL_IMAGE_NAME}" .

# Tag as latest if not already
if [ "$TAG" != "latest" ]; then
    docker tag "${FULL_IMAGE_NAME}" "${DOCKER_USERNAME}/${IMAGE_NAME}:latest"
fi

echo "Built successfully!"

# Ask for confirmation before pushing
read -p "Push to Docker Hub? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Logging in to Docker Hub..."
    docker login
    
    echo "Pushing ${FULL_IMAGE_NAME}..."
    docker push "${FULL_IMAGE_NAME}"
    
    if [ "$TAG" != "latest" ]; then
        echo "Pushing ${DOCKER_USERNAME}/${IMAGE_NAME}:latest..."
        docker push "${DOCKER_USERNAME}/${IMAGE_NAME}:latest"
    fi
    
    echo "Successfully pushed to Docker Hub!"
    echo "Image available at: https://hub.docker.com/r/${DOCKER_USERNAME}/${IMAGE_NAME}"
else
    echo "Build completed but not pushed to Docker Hub."
fi 