import json
import logging
import random
import time
import pymysql

from dataclasses import dataclass
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode, SpanKind

from .db import Client as MySQLClient
from .cache import Client as RedisClient

logger = logging.getLogger(__name__)
tracer = trace.get_tracer("otel-python-app")


@dataclass
class User(object):
    id: int
    email: str
    firstName: str
    lastName: str

    # @tracer.start_as_current_span("user-save")
    # def save(self, conn: pymysql.Connection):
    #     with tracer.start_as_current_span("app.users.save-user", kind=SpanKind.CLIENT) as span:
    #         span.set_attribute("user.id", self.id)
    #         span.set_attribute("user.email", self.email)
    #         with conn.cursor() as cursor:
    #             cursor.execute("UPDATE `users` SET email=%s, firstName=%s, lastName=%s WHERE id=%s",
    #                         (self.email, self.firstName, self.lastName, self.id))
    #         conn.commit()
    #         conn.close()

    def __serialize__(self):
        return {
            'id': self.id,
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName
        }


class UserController(object):
    def __init__(self, logger: logging.Logger, db_client: MySQLClient, cache_client: RedisClient):
        self.users = []
        self.logger = logger
        self.db = db_client
        self.cache = cache_client

    def add_user(self, user: User):
        with tracer.start_as_current_span("app.users.ctlr.add_user", kind=SpanKind.INTERNAL) as span:
            self.users.append(user)
    
    def get_users(self) -> list[User]:
        with tracer.start_as_current_span("app.users.ctlr.get_users", kind=SpanKind.CLIENT) as span:
            self.logger.debug(f'UserController.get_users()')
            cached_users = self._get_users_redis()
            self.logger.debug(f'UserController.get_users() cached_users: {cached_users}')
            if len(cached_users) == 0:
                users = self._get_users_mysql()
                self.logger.debug(f'UserController._get_users_mysql() users: {users}')
                self._cache_users(users)
            else:
                users = cached_users
            return users
        
    def _get_users_redis(self) -> list[User]:
        with tracer.start_as_current_span("app.users.ctlr.get_users.cache", kind=SpanKind.CLIENT) as span:
            self.logger.debug(f'UserController._get_users_redis()')
            users = self.cache.get_dict(key='users')
            self.logger.debug(f'UserController._get_users_redis(): users: {users}')

            # Simulate a random error
            if random.random() < 0.1:  # 10% chance
                err = ValueError("This is an intentional error.")
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(err)
                raise err
            user_objects = []
            if len(users.keys()) != 0:
                for user in users:
                    user_dict = json.loads(users[user])
                    user_objects.append(User(**user_dict))
                self.logger.debug(f'UserController._get_users_redis(): user_objects: {user_objects}')
            return user_objects

    def _get_users_mysql(self) -> list[User]:
        with tracer.start_as_current_span("app.users.ctlr.get_users.db", kind=SpanKind.CLIENT) as span:
            users = []
            self.logger.debug(f'UserController._get_users_mysql()')

            # Simulate a slow query
            time.sleep(2)
            with self.db.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM `users`")
                result = cursor.fetchall()
            self.logger.debug(f'UserController._get_users_mysql() result: {result}')
            for row in result:
                users.append(User(id=row['id'], email=row['email'], firstName=row['firstName'], lastName=row['lastName']))
            return [] if len(users) == 0 else users

    def _cache_users(self, users: list[User]) -> None:
        with tracer.start_as_current_span("app.users.ctlr.cache_users.cache", kind=SpanKind.CLIENT) as span:
            user_dict = {}
            self.logger.debug(f'UserController._cache_users(): users: {users}')
            if users is not None:
                for user in users:
                    user_dict[user.id] = json.dumps(user.__serialize__())
                self.logger.debug(f'UserController._cache_users(): user_dict: {user_dict}')
                self.cache.set_dict('users', user_dict)
            return None


