# -*- coding: utf-8 -*-
"""

───│─────────────────────────────────────
───│────────▄▄───▄▄───▄▄───▄▄───────│────
───▌────────▒▒───▒▒───▒▒───▒▒───────▌────
───▌──────▄▀█▀█▀█▀█▀█▀█▀█▀█▀█▀▄─────▌────
───▌────▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄───▋────
▀███████████████████████████████████████▄─
──▀█████ flask_does_redis ████████████▀──
─────▀██████████████████████████████▀────
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

CONFIG 

    REDIS_URL
    REDIS_HOST
    REDIS_PORT
    REDIS_DB
    REDIS_USERNAME
    REDIS_PASSWORD

HOW TO

    from flask_does_redis import RedisManager    
    app = Flask(__name__)
    r = RedisManager(app)

    -OR-

    from flask_does_redis import RedisManager
    r = RedisManager()
    def create_app():
        app = Flask(__name__)
        r.init_app(app)

    -THEN-

    conn attribute is active connection
    r.conn.ping()

    pool attribute has connection pool
    instance = redis.Redis(connection_pool=r.pool)

    we also have convenience methods get(), set(), and delete()
    r.set("foo", "bar")
    r.get("foo")
    r.delete("foo")

    more advanced usage can be accomplished via conn

    d = {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}
    r.conn.mset(d)

"""

from redis import ConnectionPool
from redis import Redis


__version__ = '0.3.2'
__author__ = '@jthop'


class RedisManager(ConnectionPool):
    def __init__(self, app=None):
        """Redis manager constructor.  Since we comply with app factory
        the constructor is put off until init_app()
        Args:
            app: Flask app beinging initialized from.
        """
        self.__version__ = __version__
        self._config = None
        self._name = None
        self.flask_app = None
        self.pool = None
        self.conn = None

        if app is not None:
            self.init_app(app)

    def _fetch_config(self):
        """
        Fetch config in the REDIS_ namespace from the app.config dict.
        """

        cfg = self.flask_app.config.get_namespace('REDIS_')
        clean = {k: v for k, v in cfg.items() if v is not None}
        self._config = clean

    def init_app(self, app):
        """the init_app method called from the app_factory
        Args:
            app: Flask app beinging initialized from
        """
        self.flask_app = app
        self._name = self.flask_app.import_name
        self._fetch_config()

        # use the url if available
        url = self._config.get('url')
        if url:
            self.pool = ConnectionPool.from_url(url)
            with self.flask_app.app_context():
                self.flask_app.logger.info(
                    f'Redis Manager pool instantiated with {url}')

        # if no url is available, hopefully the remaining config has what is needed
        else:
            self.pool = ConnectionPool(**self._config)
            with self.flask_app.app_context():
                self.flask_app.logger.info(
                    f'Redis Manager pool instantiated with {self._config}')

        # as long as we have a pool, we can create a connection instance
        if self.pool:
            self.conn = Redis(connection_pool=self.pool)

    def get(self, k):
        """
        Simple convenience wrapper
        """

        return self.conn.get(k)

    def set(self, k, v):
        """
        Simple convenience wrapper
        """

        return self.conn.set(k, v)

    def delete(self, k):
        """
        Simple convenience wrapper
        """
        
        return self.conn.delete(k)


