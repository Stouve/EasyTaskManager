FROM python:3.13-slim

# Avoid python to create .pyc files and force logs

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /code

# System dependencies to compile psycopg2 & pwdlib[argon2]
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# install poetry
RUN pip install --no-cache-dir poetry

# Copying dependencies files only first
# Allow docker to put this layer in cache as long as files don't change
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --only main --no-root

# Copying rest of code
COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]