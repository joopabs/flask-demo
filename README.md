# flask-demo

# Flask ToDo API

A simple Flask-based API for managing ToDo items. This project uses Flask-SQLAlchemy for interacting with a PostgreSQL database and supports both local and containerized deployments. Sensitive settings (like the database URL) can be managed through environment variables or Azure Key Vault.

---

## Features

- **Health Check Endpoint:** Quickly verify that the application is running.
- **CRUD Endpoints:** Create, retrieve, update, and delete ToDo items.
- **Automatic Database Setup:** Required tables are created automatically on startup.
- **Local and Secure Configuration:** Use a `.env` file for local settings or Azure Key Vault for production secrets.
- **Containerized Deployment:** Preconfigured Dockerfile and Docker Compose setup for easy cloud or local container deployment.

---

## Requirements

- **Python:** 3.13  
- **Dependency Management:** Pipenv  
- **Container Requirements (optional):** Docker & Docker Compose  

---

## Setup and Installation

### Local Development

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies:**

   Use Pipenv to install the necessary packages:

   ```bash
   pipenv install
   ```

3. **Configure Environment Variables:**

   Create a `.env` file at the project root (an example is provided in `.env.example`). For instance, to configure your database:

   ```dotenv
   DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_db
   USE_KEYVAULT=False
   ```

   If you plan to use Azure Key Vault, set `USE_KEYVAULT=True` and add the required keys.

4. **Run the Application:**

   Launch the application with:

   ```bash
   pipenv run python app.py
   ```

   The API will start in debug mode on port 5000.

### Dockerized Deployment

#### Using Docker Compose

1. **Start the Services:**

   Use Docker Compose to build and run both the API and the PostgreSQL database:

   ```bash
   COMPOSE_BAKE=true docker-compose up --build -d
   ```

2. **Stop the Services:**

   Shut down the containers when finished:

   ```bash
   docker-compose down -v
   ```

---

## API Endpoints

### Health Check

- **Method:** GET  
- **Endpoint:** `/health`  
- **Description:** Returns the current health status of the application.

   ```bash
   curl http://localhost:5000/health
   ```

### Create a ToDo

- **Method:** POST  
- **Endpoint:** `/todos`  
- **Description:** Create a new ToDo item. The payload must include a `task` attribute.

   ```bash
   curl -X POST http://localhost:5000/todos \
        -H "Content-Type: application/json" \
        -d '{"task": "Buy groceries"}'
   ```

### Retrieve All ToDos

- **Method:** GET  
- **Endpoint:** `/todos`  
- **Description:** Retrieves a list of all ToDo items.

   ```bash
   curl http://localhost:5000/todos
   ```

### Update a ToDo

- **Method:** PUT  
- **Endpoint:** `/todos/<id>`  
- **Description:** Update an existing ToDo item by its ID.

   ```bash
   curl -X PUT http://localhost:5000/todos/1 \
        -H "Content-Type: application/json" \
        -d '{"task": "Buy groceries and fruits"}'
   ```

### Delete a ToDo

- **Method:** DELETE  
- **Endpoint:** `/todos/<id>`  
- **Description:** Delete a specific ToDo item by its ID.

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