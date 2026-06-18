# Authentication Microservice

An authentication microservice built using FastAPI, MongoDB and Docker.

## Features

* User Registration
* User Login
* JWT Authentication
* Access Tokens
* Refresh Tokens
* Refresh Token Rotation
* Protected Endpoints
* User Logout
* Password Hashing using bcrypt
* Duplicate Username Prevention
* Duplicate Email Prevention
* Account Lockout Protection
* Dockerized Deployment
* Docker Compose Support

---

## Architecture

Client → FastAPI → MongoDB

The authentication service is responsible for:

* User registration
* Authentication
* JWT token issuance
* Refresh token management
* Session invalidation

MongoDB is used for:

* User storage
* Refresh token storage

---

## Tech Stack

* FastAPI
* MongoDB
* PyMongo
* Passlib (bcrypt)
* Python-JOSE
* Docker
* Docker Compose

---

## API Endpoints

### Register

POST /auth/register

Creates a new user account.

---

### Login

POST /auth/login

Authenticates a user and returns:

* Access Token
* Refresh Token

---

### Logout

POST /auth/logout

Invalidates the refresh token.

---

### Refresh Token

POST /auth/refresh

Generates a new access token and refresh token.

---

### Current User

GET /auth/me

Returns information about the authenticated user.

---

## Running Locally

```bash
docker compose up --build
```

<h5> Application: </h5>
Test the backend here: 

http://localhost:8000/docs

---

## Environment Variables

```env
SECRET_KEY=your-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MONGO_URI=mongodb://mongo:27017
```
