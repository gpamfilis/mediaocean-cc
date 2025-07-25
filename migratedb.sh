# #!/bin/bash

if [ -z "$1" ]; then
    echo "You must provide a migration message in '<message>'"
else
    cd backend
    poetry run alembic revision --autogenerate -m "$1"
    poetry run alembic upgrade head
    cd ..
    cd ..
    cd ..
fi