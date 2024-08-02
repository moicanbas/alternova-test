# Alternova - Test

This is my proposed solution to the test for backend developer in Alternova, I have named it calification app.

# Calification App

This project is a Django Rest Framework(DRF) application for qualifying students of a university.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)

## Overview

The grading application provides a series of endpoints that allow, among other things, to grade a student for a period, create, edit, read and delete students, subjects, teachers and departments, as well as validations and authentication to protect the security of the API.

## Features

- Authentication
- Scalable database
- Intuitive documentation 
- Validations
- Error handling

## Technologies Used

- Django: Web framework for building robust web applications.
- djangorestframework: Toolkit for building Web APIs in Django.
- djangorestframework-simplejwt: JWT authentication for Django REST framework.
- psycopg2-binary: PostgreSQL adapter for Python.
- python-dotenv: Loads environment variables from a .env file.
- drf-yasg: Generates OpenAPI/Swagger documentation for Django REST framework.
- cryptography: Cryptographic library for secure data handling.

## Installation

**Clone the repository:**

   ```bash
   git clone https://github.com/moicanbas/alternova-test.git
   ```

## Environment Variables
Create a .env file in the root directory of the project and add the following environment variable:
```bash
DB_NAME = 'my_database'
DB_USER = 'jhon_doe'
DB_PASSWORD = 'example123**'
DB_HOST = 'localhost'
DB_PORT = '5432'
```

Now create a virtual environment and install the requirements
```bash
virtualenv env

pip install -r requeriments.txt
```
Remember to install the virtualenv package.

Once the necessary dependencies have been installed we can run the migrations, so we can run the API
```bash
python manage.py makemigrations

python manage.py migrate
```

## Usage

1. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

2. **Run the development server:**

    This will start the development server at http://localhost:3000 or on the specified port, or available.

It is possible to create data from scratch with the available CRUDs, or you can run a script that fills the tables with dummy data.

3. **Run the script that fills tables(optional):**
    ```bash
   python populate_data.py
   ```

You can go to http://localhost:3000/docs to view API endpoints and documentation.

