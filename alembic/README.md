### Install alembic
```
pip install alembic
```

### Set `DATABASE_URL` environment variable
```
export DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/todo
```

### Install todo-api as a package
```
pip install -e .  # `-e` installs the package in development mode
```

### Generate a revision
```
alembic revision --autogenerate -m "message about revision"
```

### Run migrations
```
alembic upgrade head
```

### Documentation
http://alembic.zzzcomputing.com/en/latest/tutorial.html
