from .engine import SqlAlchemyBackend

# noinspection PyUnresolvedReferences
from .model import SqlaModel


def create_sql_storage_backend():
    return SqlAlchemyBackend()
