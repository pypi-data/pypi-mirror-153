import os
# from enum import Enum
from pathlib import Path

from samesyslib.utils import load_config


DEFAULT_ENV = "dev"
CONFIG_PATH = os.getenv("CONFIG_PATH", None)


# class Envs(Enum):
#     DEV = "dev"
#     STG = "stg"
#     PROD = "prod"


class DBParams(object):
    host = None
    schema = None
    login = None
    password = None
    port = None
    connector = "pymysql"
    parameters = {}
    connect_args = {}

    def __init__(self, **params):
        self.__dict__.update(params)


class DBConfig(object):
    def __init__(self, env=None, schema=None, bi=False, parameters={}, connect_args={}):
        self._schema = schema
        self._env = env
        self._bi = bi
        self._connect_args = connect_args
        self._parameters = parameters

        self.db_connection = None
        self.bi_connection = None

        self._change_env(env)
        self._proceed()

    def _change_env(self, env):
        # if env and env not in Envs._value2member_map_:
        #     raise Exception(f"ERROR: passed env: {env} is not valid")
        self._env = env or DEFAULT_ENV

    def _load_from_config(self):
        path = Path.home() / Path(CONFIG_PATH)
        cred = load_config(path)
        conf = cred[self._env]
        conf['parameters'] = self._parameters
        conf['connect_args'] = self._connect_args
        self.db_connection = DBParams(**conf)

        conf = cred[self._env]
        conf["schema"] = "samesystem_sisense"
        conf['parameters'] = self._parameters
        conf['connect_args'] = self._connect_args
        self.bi_connection = DBParams(**conf)

    def _load_from_env(self):
        self.db_connection = DBParams(
            host=os.getenv("DB_HOST"),
            schema=self._schema or os.getenv("SCHEMA"),
            login=os.getenv("LOGIN"),
            password=os.getenv("PASSWORD"),
            port=os.getenv("DB_PORT"),
            parameters=self._parameters,
            connect_args=self._connect_args
        )

        if self._bi:
            self.bi_connection = DBParams(
                host=os.getenv("BI_DB_HOST", os.getenv("BI_DB_HOST_SHARD1")),
                schema=os.getenv("BI_SCHEMA", os.getenv("BI_SCHEMA", "samesystem_sisense")),
                login=os.getenv("BI_LOGIN", os.getenv("BI_DB_LOGIN_SHARD1")),
                password=os.getenv("BI_PASSWORD", os.getenv("BI_DB_PASS_SHARD1")),
                port=os.getenv("BI_DB_PORT", os.getenv("BI_DB_PORT_SHARD1")),
                parameters=self._parameters,
                connect_args=self._connect_args
            )

    def _proceed(self):
        if CONFIG_PATH:
            self._load_from_config()
        else:
            self._load_from_env()

    def get_config(self):
        return self.db_connection

    def get_bi_config(self):
        if not self._bi:
            raise Exception("BI not enabled")

        return self.bi_connection
