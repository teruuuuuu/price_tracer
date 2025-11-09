#!/bin/bash

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR/infra/postgres" || exit 1


echo "Starting PostgreSQL container..."
docker-compose -f "docker-compose.yml" up -d postgres