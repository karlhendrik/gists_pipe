
#!/bin/bash

PROJECT_ROOT="/home/travis/gists_pipe"

echo "Building..."
docker-compose -f "$PROJECT_ROOT"/docker-compose.yml up --build -d