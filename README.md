# Python Django Rest API Untangling

The purpose of this project is to convert 'spaghetti' code like the sample provided in `docs/technical_task.py` and make it more readable, efficient, and maintainable.

## Table of Contents
- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)

## Introduction
This project demonstrates the best practices for refactoring and organizing Django REST API code. The goal is to transform messy and unstructured code into clean, modular, and maintainable codebases.

## Project Structure
```
DJANGO-REST-API-UNTANGLING/
│
├── django_rest_api_untangling/
│ ├── src/
│ │ ├── init.py
│ │ ├── LoggerHelper.py
│ │ ├── StatusMsg.py
│ │ ├── django_rest_api_untangler.py
│ ├── docs/
│ ├── tests/
│ ├── pyproject.toml
│ ├── README.md
│ ├── main.py
```

## Installation
To set up this project locally, follow these steps:

1. Clone the repository:
```
git clone https://github.com/your-username/django-rest-api-untangling.git
```

2. Navigate to the project directory:
```
cd django-rest-api-untangling
```

3. Install dependencies using Poetry:
```
poetry install
```

## Usage
To run the code, execute the following command:
```
poetry run django-rest-api-untangling
```

With these updates, the project structure and code organization are improved, making the code more modular, maintainable, and easier to understand. The README.md file is also updated to reflect the changes, and the Docker configuration ensures the application can be easily containerized and run in any environment.
