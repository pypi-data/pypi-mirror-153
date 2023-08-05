import os
import socket

from delphai_utils.config import get_config
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

DB_CONN_BY_PID_AND_DBNAME = {}  # (process id, db_name) -> DB_CONN

db_connection_string = get_config("database.connection_string")
default_database_name = get_config("database.name") or "main"

MAX_POOL_SIZE = 8
MAX_IDLE_TIMEOUT = 60

mongo_parameters = dict(
    host=db_connection_string,
    appname=socket.gethostname(),
    connect=False,
    maxPoolSize=MAX_POOL_SIZE,
    maxIdleTimeMS=MAX_IDLE_TIMEOUT * 1000,
)

db_client = AsyncIOMotorClient(**mongo_parameters)
db = db_client[default_database_name]
db_sync_client = MongoClient(**mongo_parameters)
db_sync = db_sync_client[default_database_name]


def get_own_db_connection(db_name: str = None):
    """
    Creates neq connection to database.
    :param db_name: use this parameter only if DB name differs from `default_database_name`
    :return: database connection
    """
    pid = os.getpid()
    if db_name is None:
        req_db_name = default_database_name

    if (pid, req_db_name) in DB_CONN_BY_PID_AND_DBNAME:
        return DB_CONN_BY_PID_AND_DBNAME[(pid, req_db_name)]
    client = MongoClient(**mongo_parameters)

    res = client[req_db_name]
    DB_CONN_BY_PID_AND_DBNAME[(pid, req_db_name)] = res
    return res
