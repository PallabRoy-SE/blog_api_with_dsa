# Blog API Created By PALLAB ROY

A RESTful API backend for a simple blogging platform, built with Python Flask. It supports user authentication (JWT), creating and managing blog posts, and adding comments.

## Features

- **User Authentication:**
  - User registration (`/api/auth/register`)[POST]
  - User login with JWT token generation (`/api/auth/login`)[POST]
  - Token refresh (`/api/auth/refresh`)[POST]
  - Get current user (`/api/auth/current-user`)[GET]
- **Blog Posts:**
  - Create a new blog post (`/api/posts`)[POST] (requires authentication)
  - Read all blog posts (`/posts`)[GET] (public, with pagination)
  - Read a single blog post with its comments (`/posts/:post_id`)[GET] (public)
  - Update a blog post (`/posts/:post_id`)[PUT] (author only, requires authentication)
  - Delete a blog post (`/posts/:post_id`)[DELETE] (author only, requires authentication)
- **Comments:**
  - Add a comment to a blog post (`/posts/:post_id/comments`)[POST] (authenticated users or anonymous with name)
  - Read all comments for a specific post (`/posts/:post_id/comments`)[GET] (included with post details)
- **Database:** Uses Flask-SQLAlchemy with SQLite.

## Tech Stack

- **Backend:** Python 3
- **Framework:** Flask
- **Database ORM:** Flask-SQLAlchemy
- **Database:** SQLite (default)
- **Authentication:** Flask-JWT-Extended
- **CORS:** Flask-CORS
- **Password Hashing:** bcrypt
- **Environment Variables:** python-dotenv

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Setup Instructions

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/PallabRoy-SE/blog_api_with_dsa.git
    cd Blog_API
    ```

2.  **Create and Activate a Virtual Environment:**

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    Create a `.env` file in the root directory (`Blog_API/`).

    ```env
    SECRET_KEY='flask_secret_key'
    JWT_SECRET_KEY='jwt_secret_key'
    DB_URI='sqlite:///../instance/data.db'
    ```

## Running the Application

1.  Run the Flask development server:
    ```bash
    python app.py
    ```
2.  The API will be accessible at `http://localhost:5000`.
