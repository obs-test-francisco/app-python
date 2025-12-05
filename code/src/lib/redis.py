import os
import redis
import logging

from dataclasses import dataclass
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode, SpanKind

tracer = trace.get_tracer("otel-python-app")

logger = logging.getLogger(__name__)


@dataclass
class RedisConfig(object):
    def __init__(self):
        self.url = os.environ.get("REDIS_URL", None)
        if self.url is not None:
            self.host = self.url.split(":")[1]
            self.port = self.url.split(":")[2].split("/")[0]
            self.db = self.url.split('/')[3]
        else:
            raise AttributeError("Must create RedisConfig object with a valid")


class RedisClient:
    def __init__(self, config: RedisConfig = RedisConfig()):
        self.config = config
        self.client = redis.from_url(url=self.config.url)

    def get_dict(self, key: str) -> dict:
        return self.client.hgetall(key)

    def set_key(self, key: str, value: str) -> None:
        self.client.set(key, value)
        return None

    def set_dict(self, key: str, value: dict) -> None:
        self.client.hmset(key, value)
        return None

    def delete_key(self, key):
        self.client.delete(key)
        return None


def get_redis_client(config: RedisConfig) -> redis.Redis:
    with tracer.start_as_current_span(name="get-redis-client", kind=SpanKind.INTERNAL) as span:
        try:
            return redis.from_url(url=config.url)
        except Exception as e:
            err = Exception(f'CONNECTION FAILED: {e}: {config.url}')
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(err)
            raise err


@tracer.start_as_current_span("redis-status")
def redis_status() -> dict:
    config = RedisConfig()
    r = get_redis_client(config)
    status = {
        "status": "OK",
        "url": config.url,
        "port": config.port,
        "db": config.db,
    }

    if not r.ping():
        status['status'] = 'FAILED'

    return status


