import os
import logging
import redis

from dataclasses import dataclass
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode, SpanKind
from opentelemetry.instrumentation.redis import RedisInstrumentor


tracer = trace.get_tracer("otel-python-app")
logger = logging.getLogger(__name__)


@dataclass
class Config(object):
    def __init__(self):
        self.url = os.environ.get("REDIS_URL", None)
        if self.url is not None:
            self.host = self.url.split(":")[1]
            self.port = self.url.split(":")[2].split("/")[0]
            self.db = self.url.split('/')[3]
        else:
            raise AttributeError("Must create RedisConfig object with a valid")


class Client(object):
    def __init__(self, config: Config=Config()):
        self.config = config
        self.client = self.connect()

    def connect(self) -> redis.client.Redis:
        with tracer.start_as_current_span(name="app.redis.connect", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system", "redis")
            span.set_attribute("db.system.name", "redis")
            try:
                pool = redis.ConnectionPool().from_url(self.config.url)
                c = redis.Redis().from_pool(pool)
                RedisInstrumentor.instrument_client(client=c)
                return c
            except Exception as e:
                err = Exception(f'CONNECTION FAILED: {e}: {self.config.url}')
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(err)
                raise err
        
    def status(self) -> dict:
        with tracer.start_as_current_span("app.redis.status", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system", "redis")
            span.set_attribute("db.system.name", "redis")
            status = {
                "status": "OK",
                "url": self.config.url,
                "port": self.config.port,
                "db": self.config.db,
            }

            if not self.client.ping():
                status['status'] = 'FAILED'

            return status
                
    def get_dict(self, key: str) -> dict:
        with tracer.start_as_current_span("app.redis.get_dict", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system", "redis")
            span.set_attribute("db.system.name", "redis")
            return self.client.hgetall(key)

    def has_lock(self) -> bool:
        with tracer.start_as_current_span("app.redis.has_lock", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system.name", "redis")
            logging.info('Checking Lock..')
            if self.client.get("flask:startup:lock"):
                logging.info('Lock FOUND!')
                return True
            logging.info('Lock NOT FOUND!')
            return False

    def lock(self) -> None:
        with tracer.start_as_current_span("app.redis.lock", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system", "redis")
            span.set_attribute("db.system.name", "redis")
            logging.info('Setting Lock..')
            self.client.setnx("flask:startup:lock", 1)
    
    def unlock(self) -> None:
        with tracer.start_as_current_span("app.redis.unlock", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system", "redis")
            span.set_attribute("db.system.name", "redis")
            logging.info('Deleting Lock..')
            self.delete_key("flask:startup:lock")

    def set_key(self, key: str, value: str) -> None:
        with tracer.start_as_current_span("app.redis.set_key", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system", "redis")
            span.set_attribute("db.system.name", "redis")
            self.client.set(key, value)
            return None

    def set_dict(self, key: str, value: dict) -> None:
        with tracer.start_as_current_span("app.redis.set_dict", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system", "redis")
            span.set_attribute("db.system.name", "redis")
            self.client.hmset(key, value)
            return None

    def delete_key(self, key):
        with tracer.start_as_current_span("app.redis.delete_key", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system", "redis")
            span.set_attribute("db.system.name", "redis")
            self.client.delete(key)
            return None
        