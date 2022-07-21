#!/bin/bash
PROJECT_ROOT="/home/travis/gists_pipe"
CONTAINER_NAME=$(docker ps --format "{{.Names}}" | grep gists_pipe_app)

echo "Running periodic checks..."
