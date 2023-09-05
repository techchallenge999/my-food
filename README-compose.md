# MyFood order & pay solution
## Requirements
* [Docker and Docker Compose](https://docs.docker.com/compose/install/)
## Usage
Follow these steps in the root directory of your local cloned repository:
- Rename the ```.env.template``` file to ```.env``` and set the environment variables with values of your choice (except POSTGRES_URL, which must be "db" to match the service name in docker-compose.yml).
- Run the following command:
    ```
    docker compose up -d db && docker compose up
    ```
## API Documentation UI
[Swagger](https://swagger.io/tools/swagger-ui/) specification is available in http://localhost:8000/docs
