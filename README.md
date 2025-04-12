# AI Tool Project

This repository contains both the frontend and backend components for the AI Tool project. The backend is built with **FastAPI**, and the frontend is built with **Next.js**.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Database Setup (Optional)](#database-setup-optional)
- [Project Structure](#project-structure)
  - [Backend](#backend)
  - [Frontend](#frontend-1)
- [Configuration](#configuration)
- [API Endpoints (Example)](#api-endpoints-example)
- [Contributing](#contributing)
- [License](#license)
- [Deployment](#deployment)
- [Testing](#testing)
- [Final Notes](#final-notes)

## Prerequisites

Before running the application, ensure that you have the following installed:

- **Python 3.x** or above
- **Node.js** and **npm** (for the frontend)
- **PostgreSQL** (if used for the database)

Additionally, you will need the following tools for development:

- **Uvicorn** for running the FastAPI backend.
- **Next.js** for running the frontend development server.

## Getting Started

Follow the instructions below to set up and run the project on your local machine.

### Backend Setup

The backend is built using **FastAPI**, and we use **uvicorn** as the ASGI server for development.

#### Steps to run the backend:

1.  **Navigate to the backend directory**:
    ```bash
    cd "Tool Automate-backend/"
    ```

2.  **Create a virtual environment**:
    Create a virtual environment to isolate the dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On MacOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4.  **Install the required dependencies**:
    Once the virtual environment is activated, install the backend dependencies listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up the environment variables**:
    Ensure that your database and other necessary services are properly configured. Create a `.env` file in the root directory of the backend and define the required variables, such as database URL, secret keys, API keys, etc.

    Example `.env` file:
    ```env
    DATABASE_URL=postgresql://username:password@localhost/ai_tool_db
    OPENAI_API_KEY=your_secret_key
    # Add other environment variables as needed
    ```

6.  **Run the backend server**:
    Start the backend server using uvicorn:
    ```bash
    uvicorn main:app --reload
    ```
    This will start the backend server, and you should see output indicating the server is running on `http://127.0.0.1:8000`.

### Frontend Setup

The frontend is built with Next.js, and we use `next dev` to run the development server.

#### Steps to run the frontend:

1.  **Navigate to the frontend directory**:
    ```bash
    cd "tool_automate-frontend/"
    ```

2.  **Install the required dependencies**:
    Install the frontend dependencies using npm or yarn:
    ```bash
    npm install
    ```
    Or if you are using yarn:
    ```bash
    yarn install
    ```

3.  **Set up the environment variables**:
    Create a `.env.local` file in the root directory of the frontend and define any necessary environment variables, such as API endpoint URLs.

    Example `.env.local` file:
    ```env
    NEXT_PUBLIC_BACKEND_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
    # Add other frontend environment variables as needed
    ```

4.  **Run the frontend development server**:
    Start the frontend server using the following command:
    ```bash
    npm run dev
    ```
    Or if you are using yarn:
    ```bash
    yarn dev
    ```
    This will start the frontend on `http://localhost:3000`.

### Database Setup (Optional)

If you're using PostgreSQL, ensure that it's set up and running. Update the `.env` file in the backend with the correct database credentials.

#### Steps to set up PostgreSQL:

1.  **Install PostgreSQL** if you haven't already. You can find installation instructions for your operating system on the official PostgreSQL website.

2.  **Create a database**: Log into the PostgreSQL shell (e.g., using `psql`) and create a new database:
    ```pgsql
    CREATE DATABASE ai_tool_db;
    ```

3.  **Update the backend's `.env` file**: Make sure to update the connection string in the `.env` file with your PostgreSQL credentials:
    ```env
    DATABASE_URL=postgresql://username:password@localhost/ai_tool_db
    ```

4.  **Run the database migrations (if applicable)** to set up the required tables. This step depends on how you are managing your database schema in the backend (e.g., using Alembic with SQLAlchemy). Refer to your backend's documentation for specific migration commands.

## Project Structure

Here's a basic overview of the project's directory structure:
