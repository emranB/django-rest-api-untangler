FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY pyproject.toml poetry.lock /code/
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install

# Copy project
COPY . /code/

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "django-rest-api-untangling"]
