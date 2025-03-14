#!/bin/bash

IMAGE_NAME="flask-todo-api-img"
CONTAINER_NAME="flask-todo-api"

echo "Cleaning up old containers and images..."

docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true
docker rmi $IMAGE_NAME 2>/dev/null || true