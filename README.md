# Dockerized Notes API

A containerized REST API built using Python Flask, SQLite, Gunicorn, Docker, and Docker Compose.

This project demonstrates practical Docker and DevOps fundamentals, including containerization, persistent storage, health checks, container networking, and non-root execution.

## Architecture


              Client
                |
                | HTTP :5000
                v
        Docker Compose
                |
                v
          Notes API
        Flask + Gunicorn
                |
                v
          SQLite Database
           /data/notes.db
                |
                v
        Docker Named Volume
             notes_data


## Technologies Used

- Python 3.12
- Flask
- SQLite
- Gunicorn
- Docker
- Docker Compose
- Linux
- Git

## Project Structure


dockerized-notes-api/
├── app/
│   ├── app.py
│   └── requirements.txt
├── screenshots/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md


## Features

- REST API for creating, listing, and deleting notes.
- Dockerized Python application.
- Gunicorn production WSGI server.
- Docker Compose deployment.
- Persistent SQLite storage using a named Docker volume.
- Container health check.
- Non-root application user for improved security.
- Automatic container restart policy.

## Prerequisites

- Linux environment
- Docker Engine
- Docker Compose

## Run the Project

Clone the repository:

git clone https://github.com/SinghP0007/dockerized-notes-api.git
cd dockerized-notes-api


Build and start:
docker compose up -d --build


Check container status:
docker compose ps


Check application logs:
docker compose logs


Application URL:
http://localhost:5000


## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application status |
| GET | `/health` | Health check |
| GET | `/notes` | List all notes |
| POST | `/notes` | Create a note |
| DELETE | `/notes/<id>` | Delete a note |

### Create a Note

curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"My First Note","content":"Learning Docker"}'

### List Notes
curl http://localhost:5000/notes


### Delete a Note
curl -X DELETE http://localhost:5000/notes/1


## Docker Operations

View running containers:
docker compose ps

View logs:
docker compose logs -f

Execute a command inside the container:
docker compose exec notes-api id

Check container health:
docker inspect --format='{{.State.Health.Status}}' \
$(docker compose ps -q notes-api)


View Docker volumes:
docker volume ls


Stop and remove containers:
docker compose down


**Note:** The named Docker volume is preserved when using `docker compose down`. The database data remains available when the application is started again.

To remove the volume and its data intentionally:
docker compose down -v

## Persistence

The SQLite database is stored at:
/data/notes.db

Docker Compose mounts a named volume at `/data`, allowing database data to survive container deletion and recreation.

## Security Practices

- Application runs as a non-root user (`appuser`).
- Dependencies are installed during image build.
- Python bytecode generation is disabled.
- Gunicorn is used instead of Flask's development server.
- Container health checks monitor application availability.

## Learning Outcomes

Through this project, I practiced:

- Writing Dockerfiles.
- Building custom Docker images.
- Running containers.
- Configuring environment variables.
- Mapping container ports.
- Managing persistent Docker volumes.
- Understanding Docker Compose networking.
- Implementing container health checks.
- Running containers with non-root privileges.
- Managing source code using Git.

## Author

Prashant

GitHub: https://github.com/SinghP0007/dockerized-notes-api.git
