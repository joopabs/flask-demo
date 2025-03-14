# flask-demo

# Flask ToDo API

This project is a simple Flask-based API for managing ToDo items. It allows you to create, retrieve, update, and delete tasks from a database using CRUD operations. The application leverages Flask-SQLAlchemy for ORM-based database interactions, is fully containerized with Docker, and uses Pipenv for dependency management.

## Features

- **Health Check Endpoint:** Quickly verify if the application is running.
- **CRUD Endpoints:** Endpoints to create, retrieve, update, and delete todo items.
- **Automatic Database Setup:** Required database tables are automatically created on startup.
- **Containerized Deployment:** Docker and Docker Compose support for simplified deployment.
- **Pipenv Workflow:** Uses Pipenv for dependency and virtual environment management.

## Requirements

- Python 3.13  
- [Pipenv](https://pipenv.pypa.io/en/latest/)

For containerized setups:
- Docker
- Docker Compose

## Setup and Installation

### Local Development

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies with Pipenv:**
   
   Ensure you have Pipenv installed. Then run:

   ```bash
   pipenv install
   ```

   This will create a virtual environment and install all required packages.

3. **Configure the Database:**

   Set the `DATABASE_URL` environment variable to point to your PostgreSQL (or another supported) instance. For example:

   ```bash
   export DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_db
   ```

4. **Run the Application:**

   Once the dependencies are installed, start the application using:

   ```bash
   pipenv run python app.py
   ```

   The application will run in debug mode and listen on port 5000.

### Dockerized Setup

This project includes a Dockerfile and a docker-compose.yaml for easy containerized deployment.

#### Using Docker

1. **Build the Docker Image:**

   ```bash
   docker build --no-cache -t flask-todo-api-img .
   ```

2. **Run the Docker Container:**

   Make sure to pass required environment variables, such as `DATABASE_URL`:

   ```bash
   docker run -d --name flask-todo-api -p 5000:5000 -e DATABASE_URL=<your_database_url> flask-todo-api-img
   ```

#### Using Docker Compose

1. **Start the Services:**

   Use Docker Compose to build and run both the API and the PostgreSQL database service:

   ```bash
   docker-compose up --build -d
   ```

2. **Shut Down the Services:**

   When finished, stop and remove the containers with:

   ```bash
   docker-compose down -v
   ```

## API Endpoints and Testing with cURL

Below are some example cURL commands to test the API endpoints.

### Health Check

- **Endpoint:** GET `/health`
- **Description:** Returns the health status of the application.

  ```bash
  curl http://localhost:5000/health
  ```

### Create a Todo

- **Endpoint:** POST `/todos`
- **Description:** Creates a new todo item. The request body expects a JSON payload with a `task` property.

  ```bash
  curl -X POST http://localhost:5000/todos \
       -H "Content-Type: application/json" \
       -d '{"task": "Buy groceries"}'
  ```

### Retrieve All Todos

- **Endpoint:** GET `/todos`
- **Description:** Retrieves a list of all todo items.

  ```bash
  curl http://localhost:5000/todos
  ```

### Update a Todo

- **Endpoint:** PUT `/todos/<id>`
- **Description:** Updates an existing todo item by its ID. Replace `<id>` with the actual todo id.

  ```bash
  curl -X PUT http://localhost:5000/todos/1 \
       -H "Content-Type: application/json" \
       -d '{"task": "Buy groceries and fruits"}'
  ```

### Delete a Todo

- **Endpoint:** DELETE `/todos/<id>`
- **Description:** Deletes a specific todo item by its ID. Replace `<id>` with the actual todo id.

  ```bash
  curl -X DELETE http://localhost:5000/todos/1
  ```

## Code Quality

- The project uses [Black](https://black.readthedocs.io/en/stable/) for consistent code formatting.

## Contributing

Contributions are welcome!  
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Ensure your code complies with the project's style guidelines (using Black for formatting).
4. Submit a pull request describing your changes.

## License

This project is licensed under the GNU General Public License v3 (GPLv3).  
For more details, please see the [LICENSE](LICENSE) file.