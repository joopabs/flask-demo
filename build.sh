#!/bin/bash

IMAGE_NAME="flask-todo-api-img"
CONTAINER_NAME="flask-todo-api"

echo "Building Docker image..."

docker build --no-cache -t $IMAGE_NAME .

if [ $? -eq 0 ]; then
  echo "Docker image built successfully."
else
  echo "Docker image build failed."
  exit 1
fi

echo "Running Docker container..."

docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME
