import os
import json
import logging

from flask import Flask
from logging.config import dictConfig

from opentelemetry.instrumentation.flask import FlaskInstrumentor


from .lib.redis import redis_status, RedisClient
from .lib.mysql import mysql_status, populate_initial_data
from .lib.users import UserController
from .lib.util import serialize_users
from .lib.otel import setup_tracer

logfile_dir = os.environ.get("LOGS_DIR", "/mnt/shared/logs")
tracer = setup_tracer()

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        },
        'json_formatter': {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'json_formatter'
        },
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'json_formatter'
        },
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "json_formatter",
            "level": "INFO",
            "filename": f'{logfile_dir}/app-log.json',
        }        
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'fileHandler']
    }
})

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app, excluded_urls="/healthz")

@app.route("/")
def index() -> str:
    return 'hello '


@app.route("/healthz")
def status() -> str:
    result = {
        "mysql": mysql_status(),
        "redis": redis_status()
    }
    return json.dumps(result)


@app.route("/users")
def get_users() -> str:
    ctlr = UserController(logger=app.logger)
    app.logger.info(f'Getting users from controller: {ctlr}')
    users = ctlr.get_users()
    app.logger.info(f'Getting users from controller: {users} ')
    return serialize_users(users)


@app.route("/flush")
def flush_redis() -> dict:
    r = RedisClient()
    r.delete_key('users')
    return {
        'status': 'OK',
    }


@app.route("/init")
def init_data() -> str:
    data = populate_initial_data()
    return json.dumps(data)

