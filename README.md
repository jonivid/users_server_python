# Flask User Management API

This Flask application provides a simple backend to manage user operations such as registration, login, user information retrieval, updating, and deletion. It leverages Flask, SQLAlchemy, and Flask-JWT-Extended for authentication and data management.

## Features

- **User Registration**: Allows new users to register.
- **User Login**: Handles user authentication and returns a JWT.
- **User Retrieval**: Fetches all users or a specific user by ID.
- **User Update**: Allows updating user details.
- **User Deletion**: Supports deleting a user by ID.

## Getting Started

### Prerequisites

- Python 3.6+
- pip
- virtualenv (optional)

### Installation

Clone the repository:
git clone https://github.com/jonivid/users_server_python.git
cd yourrepository

Set up a virtual environment (optional):
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required packages:
pip install -r requirements.txt

Create a .env file in the root directory of the project and fill it with the necessary environment variables:
SECRET_KEY=your_secret_key_here
SQLALCHEMY_DATABASE_URI=sqlite:///user_server.db
JWT_SECRET_KEY=your_very_secret_key_here

Run the application using:
flask run

This will start a development server on:
http://localhost:5000


API Endpoints
POST   /users/create_user: Register a new user.
POST   /users/login_user: Authenticate a user and return a JWT.
GET    /users: Retrieve all users (admin only).
GET    /users/<user_id>: Retrieve a specific user by user ID (admin only).
PUT    /users/<user_id>: Update user details (admin or the specified user).
DELETE /users/<user_id>: Delete a user (admin or the specified user).


## Authentication

### Obtaining a Token

To interact with most of the API endpoints, you need to be authenticated and provide a valid JWT (JSON Web Token) as a Bearer token. 
Here’s how you can obtain and use a token:

1. **Register**: If you are not already a registered user, you can create a new account by sending a POST request to `/create_user`. This endpoint requires a username and password and does not require a token.

2. **Login**: Use your credentials to log in via `/login_user`. This will authenticate your credentials and return a JWT if they are valid.

### Using the Token

For all subsequent API requests to the protected endpoints, include the obtained token as a Bearer token in the Authorization header:
"Authorization: Bearer <your_token_here>"




















