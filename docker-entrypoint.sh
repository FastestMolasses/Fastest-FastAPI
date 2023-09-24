#!/bin/sh

set -e

# Activate virtual environment
. /opt/pysetup/.venv/bin/activate

# You can put other setup logic here

# Execute passed in command
exec "$@"
