import os
import json
import logging

from flask import Flask
from logging.config import dictConfig

from opentelemetry.trace import SpanKind
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from lib.users import UserController
from lib.cache import Client as RedisClient
from lib.db import Client as MySQLClient
from lib.util import serialize_users
from lib.otel import setup_tracer

logfile_dir = os.environ.get("LOGS_DIR", "/mnt/shared/logs")
tracer = setup_tracer()
expire_lock = os.getenv("APP_EXPIRE_LOCK", False)


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
logger = logging.getLogger(__name__)

db_client = MySQLClient()
cache_client = RedisClient()

if expire_lock:
    cache_client.unlock()

if not cache_client.has_lock():
    # App is not locked, populate DB
    db_client.populate_data()
    # Lock further population attempts
    cache_client.lock()


app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

def index() -> str:
    return 'hello '


@app.route("/healthz")
def status() -> str:
    result = {
        "mysql": db_client.status(),
        "redis": cache_client.status()
    }
    return json.dumps(result)


@app.route("/users")
def get_users() -> str:
    ctlr = UserController(
        logger=app.logger,
        db_client=db_client,
        cache_client=cache_client
    )
    app.logger.info(f'Getting users from controller: {ctlr}')
    users = ctlr.get_users()
    app.logger.info(f'Getting users from controller: {users} ')
    return serialize_users(users)

@app.route("/flush")
def flush_redis() -> dict:
    r = RedisClient()
    r.delete_key('users')
    return {
        'status': 'FLUSHED',
    }
