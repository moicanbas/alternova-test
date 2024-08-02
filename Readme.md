# Alternova - Test

This is my proposed solution to the test for backend developer in Alternova, I have named it calification app.

# Calification App

This project is a Django Rest Framework(DRF) application for qualifying students of a university.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Api and Endpoints documentation](#api-and-endpoints-documentation)

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

## Requirements

- PostgreSQL
- Python

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

## Api and Endpoints documentation

To test the API in postman or other tester it is necessary to be logged in.
You can do this by calling the endpoint api/v1/accounts/login/.

```bash
{
  "username": "username",
  "password": "password"
}
```

This will return the token that will be needed to test all endpoints.

```bash
{
"refresh": "refresh_token",
"access": "access_token ",
"user": {
   "id": "id",
   "username": "example",
   "identification": "example",
   "first_name": "example",
   "last_name": "example",
   "email": "example@example.com",
   "groups": [],
   "user_permissions": [],
   "is_teacher": false,
   "is_student": false,
   "cellphone": "example"
}
```

It is necessary to keep the refresh token and the access token.

When calling an endpoint, it is necessary to indicate in the headers the token

```bash
Bearer access_token
```

## **Endpoints required in the test:**


### 1. Student Enrollment in a List of Subjects
**Endpoint:** `/api/v1/calificaciones/inscription/`

**Request:**
```json
{
  "inscription_date": "2024-08-02",
  "subjects": [1, 2, 3],
  "period": 1
}
```
### 2. Get the List of Subjects a Student is Enrolled In
**Endpoint:** `/api/v1/calificaciones/subjects-list/?period=id_period`

### 3. Get the List of Approved Subjects and General Average Score
**Endpoint:** `/api/v1/calificaciones/subjects-approval-list/?period=id_period`

### 4. Teacher Assigned to Multiple Subjects
**Endpoint:** `/api/v1/calificaciones/teacher-subject/` (CRUD for teacher-subject assignments)

### 5. Get the List of Subjects Assigned to a Teacher
**Endpoint:** `/api/v1/calificaciones/teacher-subject-list/`

### 6. Get the List of Students for Each Subject a Teacher is Assigned To
**Endpoint:** `/api/v1/calificaciones/teacher-student-list/`

### 7. Finalize Subject and Grade Each Student
**Endpoint:** `/api/v1/calificaciones/grade-student/`
**Request:**
```json
{
  "qualification": 5,
  "subject": 3,
  "student": 1
}
```
### 8. Get the Grades of Students in Teacher's Subjects
**Endpoint:** `/api/v1/calificaciones/student-grades/`
