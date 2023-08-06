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

    app = Flask(__name__)
    r = redis_factory.RedisFactory(app)

    -OR-

    r = redis_factory.RedisFactory()
    def create_app():
        app = Flask(__name__)
        h.init_app(app)

    -THEN-

    redis_instance = redis.Redis(connection_pool=r.pool)
    or
    obj.method_that_needs_redis(r.redis)

"""

from redis import ConnectionPool


__version__ = '0.2.2'
__author__ = '@jthop'


class RedisFactory(ConnectionPool):
    def __init__(self, app=None):
        """Redis factory constructor.  Since we comply with app factory
        the constructor is put off until init_app()
        Args:
            app: Flask app beinging initialized from.
        """
        self.__version__ = __version__
        self._config = None
        self._name = None
        self.flask_app = None
        self.pool = None
        self.redis = None

        if app is not None:
            self.init_app(app)

    def _fetch_config(self):
        """
        Fetch config in the APP_REDIS_ namespace from the app.config dict.
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

        url = self._config.get('url')
        if url:
            self.pool = ConnectionPool.from_url(url)
            with self.flask_app.app_context():
                self.flask_app.logger.info(
                    f'Redis Factory pool instantiated with {url}')
        else:
            self.pool = ConnectionPool(**self._config)
            with self.flask_app.app_context():
                self.flask_app.logger.info(
                    f'Redis Factory pool instantiated with {self._config}')

        if self.pool:
            self.redis = Redis(connection_pool=self.pool)

