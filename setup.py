"""Setup script to install `todo-api` as a package"""
from setuptools import setup

setup(
    name='todo',
    packages=['todo'],
    include_package_data=True,
    install_requires=[
        "connexion",
        "flask",
        "flask-cors",
        "gunicorn",
        "marshmallow",
        "psycopg2",
        "python-jose",
        "sqlalchemy",
    ],
)
