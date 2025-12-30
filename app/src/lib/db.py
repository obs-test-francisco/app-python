import os
import time
import logging
import pymysql

from dataclasses import dataclass
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode, SpanKind
from opentelemetry.instrumentation.pymysql import PyMySQLInstrumentor


logger = logging.getLogger(__name__)
tracer = trace.get_tracer("otel-python-app")

@dataclass
class Config(object):
    def __init__(self):
        self.host = os.environ.get("MYSQL_HOST", "localhost")
        self.user = os.environ.get("MYSQL_USER", "hackweek")
        self.password = os.environ.get("MYSQL_PASSWORD", "password")
        self.db = os.environ.get("MYSQL_DB", "hackweek")
        self.port = 3306

class Client(object):
    def __init__(self, config: Config=Config()):
        self.config = config
        conn = self.connect()
        self.conn = PyMySQLInstrumentor().instrument_connection(
            conn,
            enable_commenter=True,
            commenter_options={
                "db_driver": True,
                "mysql_client_version": True
            }
        )
    
    def connect(self) -> pymysql.Connection:
        with tracer.start_as_current_span(name="app.mysql.connect", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system", "mysql")
            span.set_attribute("db.system.name", "mysql")
            reconnect_max_tries = 10
            for attempt in range(reconnect_max_tries):
                try:
                    return pymysql.Connect(host=self.config.host,
                                        user=self.config.user,
                                        password=self.config.password,
                                        database=self.config.db,
                                        port=3306,
                                        connect_timeout=10,
                                        cursorclass=pymysql.cursors.DictCursor
                    )
                except Exception as e:
                    if attempt == reconnect_max_tries -1:
                        err = Exception(f'CONNECTION FAILED: {e}: {self.config.host}:{self.config.port}')
                        span.set_status(Status(StatusCode.ERROR))
                        span.record_exception(err)
                        raise err
                    else:
                        logger.warning(f'Connection attempt {attempt + 1}/{reconnect_max_tries} failed: {e}. Retrying...')
                        time.sleep(2)
            raise Exception('CONNECTION FAILED: Unable to connect after all retries')

    
    def status(self) -> dict:
        with tracer.start_as_current_span(name="app.mysql.status", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system", "mysql")
            span.set_attribute("db.system.name", "mysql")
            status = {
                "status": "OK",
                "host": self.config.host,
                "port": self.config.port,
                "user": self.config.user,
                "db": self.config.db,
            }
            if not self.conn.open:
                span.set_status(Status(StatusCode.ERROR))
                status['status'] = 'FAILED'

            return status

    def populate_data(self) -> list[dict]:
        with tracer.start_as_current_span(name="app.mysql.populate_data", kind=SpanKind.CLIENT) as span:
            span.set_attribute("db.system", "mysql")
            span.set_attribute("db.system.name", "mysql")
            logger.info("app.mysql.populate_data(): Initializing Database")
            data = [
                {
                    'email': 'alice@example.com',
                    'firstName': 'Alice',
                    'lastName': 'Smith'
                },
                {
                    'email': 'bob@example.com',
                    'firstName': 'Bob',
                    'lastName': 'Jones'
                },
                {
                    'email': 'charlie@example.com',
                    'firstName': 'Charlie',
                    'lastName': 'Brown'
                },
            ]
            with self.conn.cursor() as cursor:
                cursor.execute("CREATE TABLE IF NOT EXISTS `users` ("
                            "id INT AUTO_INCREMENT PRIMARY KEY, "
                            "email VARCHAR(255) NOT NULL, "
                            "firstName VARCHAR(255) NOT NULL, "
                            "lastName VARCHAR(255) NOT NULL)")
                for user in data:
                    cursor.execute("SELECT * FROM `users` WHERE email=%s", (user['email'],))
                    result = cursor.fetchall()
                    if len(result) > 0:
                        continue
                    else:
                        cursor.execute("INSERT INTO `users` (email, firstName, lastName) VALUES (%s, %s, %s)",
                                (user['email'], user['firstName'], user['lastName']))
            self.conn.commit()
            return data
