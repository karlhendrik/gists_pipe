
#!/bin/bash
PROJECT_ROOT="/home/travis/gists_pipe"
APP_URL=$(env | grep APP_URL | cut -d "=" -f2)
NETWORK_NAME=$(docker network ls --format "{{.Name}}" | grep nginx)
CONTAINER_NAME=$(docker ps --format "{{.Names}}" | grep gists_pipe_app)

echo "Building..."
echo "Replacing default placeholder with $APP_URL and connect to network $NETWORK_NAME"
sed -i "s/http:\/\/localhost:8000/${APP_URL}/g" "$PROJECT_ROOT"/app/static/js/main.js
docker-compose -f "$PROJECT_ROOT"/docker-compose.yml up --build -d
docker network connect "$NETWORK_NAME" "$CONTAINER_NAME"