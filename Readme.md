---

# CourseHub FastAPI Application

## Description

This repository contains a FastAPI application for managing courses, integrated with MongoDB. The application is containerized using Docker and can be easily deployed using Docker Compose. The CI/CD pipeline is set up with GitHub Actions to automate the build, test, and deployment processes.

## Environment Variables

The following environment variables are required for the application to run:

- `MONGO_URL`: MongoDB connection URL.
- `MONGO_DB`: MongoDB database name.

These variables should be defined in a `.env` file in the root directory of the project.

## Secrets

The following secrets need to be added to your GitHub repository for the CI/CD pipeline to work:

- `DOCKER_USERNAME`: Your Docker Hub username.
- `DOCKER_PASSWORD`: Your Docker Hub password.
- `MONGO_URL`: MongoDB connection URL.
- `MONGO_DB`: MongoDB database name.

## Usage Instructions

### Clone the Repository

```bash
git clone https://github.com/abhishekHegde2000/coursehub-app.git
cd coursehub-app
```

### Create a `.env` File

Create a `.env` file in the root directory with the following content:

```plaintext
MONGO_URL=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority
MONGO_DB=<your-database-name>
```

### Build and Run the Docker Image

To build and run the Docker image locally, use Docker Compose:

```bash
docker-compose up -d
```

### Access the Application

The application will be available at [http://localhost:8000](http://localhost:8000).

### Run Tests

To run the tests, use the following command:

```bash
docker-compose exec app pytest
```

## CI/CD Pipeline

The CI/CD pipeline is configured using GitHub Actions. It performs the following steps:

1. Build the Application:

   - Checks out the code.
   - Sets up Python.
   - Installs dependencies.
   - Runs tests.
2. Build and Push Docker Image:

   - Logs in to Docker Hub.
   - Builds the Docker image.
   - Pushes the Docker image to Docker Hub.
3. Deploy with Docker Compose:

   - Deploys the application using Docker Compose.

## Using the Docker Image

If you want to use the Docker image directly from Docker Hub, follow these steps:

### Pull the Docker Image

```bash
docker pull ahegde2021/coursehub-app:latest
```

### Run the Docker Container

```bash
docker run -d -p 8000:8000 --env-file .env ahegde2021/coursehub-app:latest
```

### Access the Application

The application will be available at [http://localhost:8000](http://localhost:8000).

---

By following these instructions, you can easily set up and run the CourseHub application on your local machine or deploy it using Docker Hub and Docker Compose.

---

Feel free to adjust any placeholders (`<username>`, `<password>`, `<cluster-url>`, `<dbname>`, `<your-database-name>`, `<your-docker-username>`, `<your-docker-password>`) with actual values as per your setup.
