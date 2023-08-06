import importlib
import os

from aiohttp import web

from jija.middleware import Middleware
from jija.utils.collector import collect_subclasses
from jija.command import Command


class App:
    def __init__(self, *, name, path, aiohttp_app=None, parent=None):
        """
        :type name: str
        :type path: jija.utils.path.Path
        :type aiohttp_app: web.Application
        :type parent: App
        """

        self.__parent = parent
        if parent:
            parent.add_child(self)

        self.__path = path
        self.__name = name
        self.__is_core = aiohttp_app is not None

        self.__routes = None
        self.__database = None
        self.__middlewares = None
        self.__commands = None

        self.__aiohttp_app = None

        self.__childes = []
        self.__load(aiohttp_app)

    @property
    def parent(self):
        """:rtype: App"""
        return self.__parent

    @property
    def name(self):
        """:rtype: str"""
        return self.__name

    @property
    def routes(self):
        """:rtype: list"""
        return self.__routes

    @property
    def database(self):
        """:rtype: file"""
        return self.__database

    @property
    def middlewares(self):
        """:rtype: list[Middleware]"""
        return self.__middlewares

    @property
    def aiohttp_app(self):
        """:rtype: web.Application"""
        return self.__aiohttp_app

    @property
    def childes(self):
        """:rtype: list[App]"""
        return self.__childes

    @property
    def path(self):
        """:rtype: jija.utils.path.Path"""
        return self.__path

    @property
    def commands(self):
        """:rtype: list[str]"""
        return self.__commands

    @property
    def database_config(self):
        """
        :rtype: list[file]
        """

        database_modules = ['aerich.models'] if self.__is_core else []

        if self.__database:
            database_modules.append((self.__path + 'database').python)

        return database_modules

    def __load(self, aiohttp_app=None):
        """
        :type aiohttp_app: web.Application
        """

        self.__routes = self.__get_routes(self.__path)
        self.__database = self.__get_database(self.__path)
        self.__middlewares = self.__get_middlewares(self.__path)
        self.__commands = self.__get_commands(self.__path)

        self.__aiohttp_app = self.get_aiohttp_app(aiohttp_app)

    @staticmethod
    def __get_routes(path):
        """
        :type path: jija.utils.path.Path
        :rtype: list
        """

        routes_path = path + 'routes.py'

        if os.path.exists(routes_path.system):
            routes_module = importlib.import_module(routes_path.python)
            if not hasattr(routes_module, 'routes'):
                return []

            return getattr(routes_module, 'routes')
        return []

    @staticmethod
    def __get_database(path):
        """
        :type path: jija.utils.path.Path
        :rtype: file
        """

        database_path = path + 'database.py'
        if os.path.exists(database_path.system):
            return importlib.import_module(database_path.python)

    @staticmethod
    def __get_middlewares(path):
        """
        :type path: jija.utils.path.Path
        :rtype: list[Middleware]
        """

        middlewares_path = path + 'middlewares.py'
        if os.path.exists(middlewares_path.system):
            raw_middlewares = importlib.import_module(middlewares_path.python)
            middlewares = collect_subclasses(raw_middlewares, Middleware)
            return list(map(lambda item: item(), middlewares))

        return []

    @staticmethod
    def __get_commands(path):
        """
        :type path: jija.utils.path.Path
        :rtype: list[str]
        """

        commands = {}
        commands_path = path + 'commands'
        if os.path.exists(commands_path.system):
            for file in os.listdir(commands_path.system):
                if file.endswith('.py') and not file.startswith('_'):
                    command_path = commands_path + file.replace('.py', '')
                    command_module = importlib.import_module(command_path.python)

                    command = list(collect_subclasses(command_module, Command))
                    if command:
                        commands[file.replace('.py', '')] = command[0]

        return commands

    @staticmethod
    def is_app(path):
        """
        :type path: jija.utils.path.Path
        :rtype: bool
        """

        return os.path.isdir(path.system) and os.path.exists((path + 'app.py').system) and\
               not path.has_protected_nodes()

    def get_aiohttp_app(self, aiohttp_app=None):
        """
        :type aiohttp_app: web.Application
        :rtype: web.Application
        """

        aiohttp_app = aiohttp_app or web.Application()

        aiohttp_app.middlewares.extend(self.__middlewares)
        aiohttp_app.add_routes(self.__routes)

        return aiohttp_app

    def add_child(self, child):
        """
        :type child: App
        """

        self.__childes.append(child)
