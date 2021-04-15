# Elenas Tasks

## Prerequisites

- Python v3.9
- Docker v19
- Docker Compose v1.26

## Docker Installation

- Create environment variables:

  - Create `env` files into `envs/local/` directory:

    ```sh
    cp envs/local/.env.app.example envs/local/.env.app && cp envs/local/.env.db.example envs/local/.env.db
    ```
    - Replace default values to the `.envs` values.

- Build services:

  ```sh
  docker-compose build
  ```

- Startup services:

  ```sh
  docker-compose up
  ```

- Create superuser

  ```sh
  docker exec -it django_app python manage.py createsuperuser
  ```

## Production deployment
To test this project please visit [https://www.dandresfsoto.com/](https://www.dandresfsoto.com/)
