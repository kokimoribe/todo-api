##  About
RESTful API for a todo app.

API is deployed on Heroku. Give it a try:
https://todo-api-rd7qf9.herokuapp.com/v1/ui/#!/boards/todo_api_get_boards

Built using:
- [OpenAPI/Swagger Specification](https://github.com/OAI/OpenAPI-Specification)
- [connexion](https://github.com/zalando/connexion)
- [SQLAlchemy](https://github.com/zzzeek/sqlalchemy)
- [marshmallow](https://github.com/marshmallow-code/marshmallow)

Source
https://gitlab.com/koki.moribe/todo-api

Mirror
https://github.com/kokimoribe/todo-api


## Development
1. Checkout repo
    ```bash
    git clone git@gitlab.com:koki.moribe/todo-api.git
    ```

1. Install `todo` package in development mode:
    ```bash
    # Assumes python >= 3.5
    cd todo-api
    pip install -r requirements.txt
    pip install -e .
    ```

1. Setup a PostgreSQL server set its database url as an environment variable
    ```bash
    export DATABASE_URL=postgres://username:password@host:port/database
    ```

1. Run the app
    ```bash
    python app.py
    ```

1. Swagger UI can be viewed at http://localhost:9090/v1/ui

## Running via `docker-compose`
1. Install [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/engine/installation/)

1. Run docker-compose
```bash
docker-compose up
```

1. Open browser and go to: http://localhost:9090/v1/ui



## Why?
My main motivations for this project were to try out [connexion](https://github.com/zalando/connexion) and [Heroku](https://www.heroku.com/
)

My experience with these two tools are documented in [notes.md](./notes.md)
