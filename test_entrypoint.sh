#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"

if [[ ! -e /${CONTAINER_FIRST_STARTUP} ]]; then
    touch /${CONTAINER_FIRST_STARTUP}
    # Apply database migrations
    echo "Apply database migrations"
    alembic upgrade head

    # Run tests
    echo "Running tests"
    pytest -vv
fi

echo "Starting the application"
uvicorn run:app --host 0.0.0.0 --port 8000 --reload
